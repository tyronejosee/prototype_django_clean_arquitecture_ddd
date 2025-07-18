from unittest.mock import patch, Mock
from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.cart.domain.entities.cart import Cart
from apps.cart.domain.exceptions import (
    CartDomainError,
    CartItemNotFoundError,
    CartNotFoundError,
)
from apps.cart.presentation.controllers.cart_controller import CartController
from apps.cart.presentation.controllers.cart_item_controller import CartItemController
from apps.cart.presentation.controllers.cart_preview_controller import (
    CartPreviewController,
)


@pytest.fixture
def fake_user() -> Mock:
    user = Mock()
    user.id = uuid4()
    return user


@pytest.fixture
def fake_cart(fake_user: Mock) -> Cart:
    return Cart(
        id=uuid4(),
        user_id=fake_user.id,
        items=[],
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def preview_payload() -> dict:
    return {
        "user_id": str(uuid4()),
        "items": [
            {
                "product_id": str(uuid4()),
                "quantity": 2,
            },
            {
                "product_id": str(uuid4()),
                "quantity": 1,
            },
        ],
    }


@pytest.fixture
def preview_response() -> dict:
    return {
        "subtotal": "100.00",
        "taxes": "19.00",
        "total": "119.00",
    }


@pytest.fixture
def item_id() -> UUID:
    return uuid4()


def test_cart_get_success(fake_user: Mock, fake_cart: Cart) -> None:
    # Given: a user and a cart
    factory = APIRequestFactory()
    request = factory.get("/cart")
    force_authenticate(request, user=fake_user)

    # When: retrieving the cart
    with patch(
        "apps.cart.presentation.controllers.cart_controller.get_get_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.return_value = fake_cart
        mock_provider.return_value = use_case

        response = CartController.as_view()(request)

    # Then: the cart is returned with the expected user_id and repo.get called once
    assert response.status_code == status.HTTP_200_OK
    use_case.execute.assert_called_once_with(user_id=fake_user.id)


def test_cart_get_not_found(fake_user: Mock) -> None:
    # Given: a user with no existing cart
    factory = APIRequestFactory()
    request = factory.get("/cart")
    force_authenticate(request, user=fake_user)

    # When: trying to retrieve the cart
    with patch(
        "apps.cart.presentation.controllers.cart_controller.get_get_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.side_effect = CartNotFoundError("Cart not found.")
        mock_provider.return_value = use_case

        response = CartController.as_view()(request)

    # Then: a 404 is returned with 'Cart not found.' detail
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Cart not found."  # type: ignore[union-attr] # noqa: E501


def test_cart_post_success(fake_user: Mock, fake_cart: Cart) -> None:
    # Given: a user and a valid cart creation payload
    factory = APIRequestFactory()
    payload = {"items": []}
    request = factory.post("/cart", payload, format="json")
    force_authenticate(request, user=fake_user)

    # When: creating the cart
    with patch(
        "apps.cart.presentation.controllers.cart_controller.get_create_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.return_value = fake_cart
        mock_provider.return_value = use_case

        response = CartController.as_view()(request)

    # Then: the cart is created and returned with 201 status
    assert response.status_code == status.HTTP_201_CREATED
    use_case.execute.assert_called_once()
    assert response.data["user_id"] == str(fake_user.id)  # type: ignore[union-attr] # noqa: E501


def test_cart_post_invalid_domain(fake_user: Mock) -> None:
    # Given: a user with a domain error during cart creation
    factory = APIRequestFactory()
    payload = {"items": []}
    request = factory.post("/cart", payload, format="json")
    force_authenticate(request, user=fake_user)

    # When: creating the cart and a domain error is raised
    with patch(
        "apps.cart.presentation.controllers.cart_controller.get_create_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.side_effect = CartDomainError("Cart already exists.")
        mock_provider.return_value = use_case

        response = CartController.as_view()(request)

    # Then: a 400 is returned with 'Cart already exists.' detail
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Cart already exists."  # type: ignore[union-attr] # noqa: E501


def test_cart_put_success(fake_user: Mock, fake_cart: Cart) -> None:
    # Given: a user and a valid cart update payload
    factory = APIRequestFactory()
    payload = {"items": []}
    request = factory.put("/cart", payload, format="json")
    force_authenticate(request, user=fake_user)

    # When: updating the cart
    with patch(
        "apps.cart.presentation.controllers.cart_controller.get_update_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.return_value = fake_cart
        mock_provider.return_value = use_case

        response = CartController.as_view()(request)

    # Then: the cart is updated and returned with 200 status
    assert response.status_code == status.HTTP_200_OK
    use_case.execute.assert_called_once()
    assert response.data["user_id"] == str(fake_user.id)  # type: ignore[union-attr] # noqa: E501


def test_cart_put_not_found(fake_user: Mock) -> None:
    # Given: a user with no cart to update
    factory = APIRequestFactory()
    payload = {"items": []}
    request = factory.put("/cart", payload, format="json")
    force_authenticate(request, user=fake_user)

    # When: updating the cart and it does not exist
    with patch(
        "apps.cart.presentation.controllers.cart_controller.get_update_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.side_effect = CartNotFoundError("Cart not found.")
        mock_provider.return_value = use_case

        response = CartController.as_view()(request)

    # Then: a 404 is returned with 'Cart not found.' detail
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Cart not found."  # type: ignore[union-attr] # noqa: E501


def test_patch_cart_item_success(
    fake_user: Mock, fake_cart: Cart, item_id: UUID
) -> None:
    # Given: a user and a valid item ID to update
    factory = APIRequestFactory()
    request = factory.patch(f"/cart/items/{item_id}", {"quantity": 2}, format="json")
    force_authenticate(request, user=fake_user)

    # When: patching the cart item
    with patch(
        "apps.cart.presentation.controllers."
        "cart_item_controller.get_patch_cart_item_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.return_value = fake_cart
        mock_provider.return_value = use_case

        response = CartItemController.as_view()(request, item_id=item_id)

    # Then: the item is updated successfully and 200 status is returned
    assert response.status_code == status.HTTP_200_OK
    use_case.execute.assert_called_once()


def test_patch_cart_item_not_found(fake_user: Mock, item_id: UUID) -> None:
    # Given: a user with an item ID that does not exist
    factory = APIRequestFactory()
    request = factory.patch(f"/cart/items/{item_id}", {"quantity": 2}, format="json")
    force_authenticate(request, user=fake_user)

    # When: patching the item and it is not found
    with patch(
        "apps.cart.presentation.controllers."
        "cart_item_controller.get_patch_cart_item_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.side_effect = CartItemNotFoundError("Item not found.")
        mock_provider.return_value = use_case

        response = CartItemController.as_view()(request, item_id=item_id)

    # Then: a 404 is returned with 'Item not found.' detail
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Item not found."  # type: ignore[union-attr] # noqa: E501


def test_patch_cart_item_invalid_quantity(fake_user: Mock, item_id: UUID):
    # Given: a user and an invalid quantity for the item
    factory = APIRequestFactory()
    request = factory.patch(f"/cart/items/{item_id}", {"quantity": 20}, format="json")
    force_authenticate(request, user=fake_user)

    # When: patching the item with invalid quantity
    with patch(
        "apps.cart.presentation.controllers."
        "cart_item_controller.get_patch_cart_item_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.side_effect = CartDomainError(
            "Quantity must be between 1 and 10."
        )
        mock_provider.return_value = use_case

        response = CartItemController.as_view()(request, item_id=item_id)

    # Then: a 400 is returned with 'Quantity must be between 1 and 10.'
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Quantity must be between 1 and 10."  # type: ignore[union-attr] # noqa: E501


def test_delete_cart_item_success(
    fake_user: Mock, fake_cart: Cart, item_id: UUID
) -> None:
    # Given: a user and an existing item in the cart
    factory = APIRequestFactory()
    request = factory.delete(f"/cart/items/{item_id}")
    force_authenticate(request, user=fake_user)

    # When: deleting the item from the cart
    with patch(
        "apps.cart.presentation.controllers."
        "cart_item_controller.get_delete_cart_item_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.return_value = fake_cart
        mock_provider.return_value = use_case

        response = CartItemController.as_view()(request, item_id=item_id)

    # Then: the item is deleted and 200 status is returned
    assert response.status_code == status.HTTP_200_OK
    use_case.execute.assert_called_once_with(user_id=fake_user.id, item_id=item_id)


def test_delete_cart_item_not_found(fake_user: Mock, item_id: UUID) -> None:
    # Given: a user and a non-existent item ID
    factory = APIRequestFactory()
    request = factory.delete(f"/cart/items/{item_id}")
    force_authenticate(request, user=fake_user)

    # When: trying to delete the non-existent item
    with patch(
        "apps.cart.presentation.controllers."
        "cart_item_controller.get_delete_cart_item_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.side_effect = CartItemNotFoundError("Item not found.")
        mock_provider.return_value = use_case

        response = CartItemController.as_view()(request, item_id=item_id)

    # Then: a 404 is returned with 'Item not found.' detail
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Item not found."  # type: ignore[union-attr] # noqa: E501


def test_cart_preview_success(
    fake_user: Mock, preview_payload: dict, preview_response: dict
) -> None:
    # Given: a user and a valid preview payload
    factory = APIRequestFactory()
    request = factory.post("/cart/preview", preview_payload, format="json")
    force_authenticate(request, user=fake_user)

    # When: requesting a cart preview
    with patch(
        "apps.cart.presentation.controllers."
        "cart_preview_controller.get_preview_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.return_value = preview_response
        mock_provider.return_value = use_case

        response = CartPreviewController.as_view()(request)

    # Then: the preview is returned with 200 status and correct totals
    assert response.status_code == status.HTTP_200_OK
    assert response.data == preview_response  # type: ignore[union-attr]
    use_case.execute.assert_called_once()


def test_cart_preview_invalid(fake_user: Mock, preview_payload: dict) -> None:
    # Given: a user and a preview payload with invalid data
    factory = APIRequestFactory()
    request = factory.post("/cart/preview", preview_payload, format="json")
    force_authenticate(request, user=fake_user)

    # When: requesting a cart preview and a domain error occurs
    with patch(
        "apps.cart.presentation.controllers."
        "cart_preview_controller.get_preview_cart_use_case"
    ) as mock_provider:
        use_case = Mock()
        use_case.execute.side_effect = CartDomainError("Invalid item quantity")
        mock_provider.return_value = use_case

        response = CartPreviewController.as_view()(request)

    # Then: a 400 is returned with 'Invalid item quantity' detail
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Invalid item quantity"  # type: ignore[union-attr] # noqa: E501
