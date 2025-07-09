# 📋 Functional Specifications

> [Disclaimer](../DISCLAIMER.md)

## 1. Introduction

This document describes the business rules, flows, and edge cases for the grocery and food store API, inspired by the Líder Chile business model.

The API is built following Clean Architecture and Domain-Driven Design (DDD) principles, implemented with Django and Django REST Framework, using PostgreSQL as the database and Docker Compose for service orchestration.

## 2. Main Business Rules

### 2.1 Product Management

- Each product must have a unique SKU, name, description, category, base price, and stock.
- Products may have discounted prices, which must fall within defined ranges (e.g., discount between 0% and 50%).
- Stock must be updated automatically upon sales confirmation or cancellations.
- Selling products with zero stock is not allowed.

### 2.2 Categories

- Categories organize products to facilitate search and navigation.
- Categories can be active or inactive; only active ones appear in the store.

### 2.3 Users and Roles

- Users can be customers or administrators.
- Customers can browse products, create orders, and view their history.
- Administrators can manage products, categories, and orders.

### 2.4 Orders and Payments

- Orders contain one or more products with specific quantities.
- The order total is the sum of the unit price times quantity, applying current discounts.
- Stock availability must be validated before confirming the order.
- Possible order statuses: Pending, Confirmed, Preparing, Dispatching, Delivered, Cancelled.

### 2.5 Inventory and Stock

- Stock must be controlled in real-time to prevent overselling.
- A history of stock movements (inbound, outbound) must be recorded.

### 2.6 Security

- Communications must be authenticated and authorized using JWT tokens.
- Sensitive information must be encrypted in transit and at rest where applicable.

## 3. Key Flows

### 3.1 Purchase Flow

1. Customer browses active products.
2. Adds products to the cart (client-side).
3. Requests order creation with products and quantities.
4. API validates stock, calculates total, and creates order in 'Pending' status.
5. Customer makes payment (outside or integrated with API).
6. API updates status to 'Confirmed' and reduces stock.
7. Administrator processes order and updates status accordingly.
8. Customer receives status notifications.

### 3.2 Product Management (Administrator)

1. Administrator creates/modifies/deletes products.
2. On create/modify, required fields and business rules are validated.
3. Stock can be manually adjusted for inbound and outbound movements.

## 4. Edge Cases

- Purchase attempts with insufficient stock must return a specific error.
- Order cancellations after confirmation must replenish stock.
- Discounts outside allowed ranges must be rejected.
- Unauthorized users cannot access administrative resources.
- Inactive products or categories do not appear in public listings.
- Multiple user sessions must respect stock consistency.
