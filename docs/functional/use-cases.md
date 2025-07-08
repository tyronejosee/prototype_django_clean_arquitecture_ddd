# 📋 Use Cases / User Stories

> [Disclaimer](../DISCLAIMER.md)

## 1. Customer Users

### 1.1 As a customer, I want to see a list of active products to choose what to buy

- The system shows products with available stock, including their price and possible discount.
- Products can be filtered by category.

### 1.2 As a customer, I want to create an order with selected products and quantities

- The system validates that the stock is sufficient.
- The final total of the order is calculated.
- The order is saved with status 'Pending'.

### 1.3 As a customer, I want to see the status of my orders to know their current stage

- Updated statuses are shown (Confirmed, Preparing, Shipping, etc.).

### 1.4 As a customer, I want to cancel a pending order to avoid making the purchase

- The order is canceled and the reserved stock is released.

## 2. Administrator Users

### 2.1 As an administrator, I want to create new products to offer more variety in the store

- I must be able to enter valid data and comply with business rules.

### 2.2 As an administrator, I want to modify existing products to update prices, stock, or information

- Changes are validated and applied in real-time.

### 2.3 As an administrator, I want to manage categories to organize products

- I can activate or deactivate categories.

### 2.4 As an administrator, I want to change the status of an order to reflect its progress in preparation and shipping

- I can update statuses and generate notifications to the customer.

## 3. Cross-Cutting Use Cases

### 3.1 Authentication and Authorization

- Users must log in to access personalized features.
- The system protects sensitive endpoints with roles and permissions.

### 3.2 Notifications

- The system sends notifications on key events (order confirmed, shipped, etc.).
