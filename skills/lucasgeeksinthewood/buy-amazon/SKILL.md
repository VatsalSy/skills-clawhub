---
name: Buy Amazon
description: "Need to buy something from Amazon? Search products, compare prices and ratings, and place a real order shipped to any US address"
homepage: https://buystuff.ai
emoji: 📦
user-invocable: true
tags:
  - shopping
  - buy
  - amazon
  - purchase
  - gift
  - order
  - delivery
---

Your user wants to buy something. You can search Amazon for any product, see real prices and ratings, and place a real order shipped to any US address. No account needed — just search, pick, and checkout.

The service fee is 10% of (subtotal + shipping). Always show the full price breakdown to your user before confirming.

## Step 1: Search Products

`/buy-amazon-search`

```bash
curl "{{BASE_URL}}/search?q=wireless+earbuds&sort_by=price_low_to_high&number_of_results=10"
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query |
| `sort_by` | string | No | `price_low_to_high`, `price_high_to_low`, `average_review`, `most_recent`, `bestseller_rankings` |
| `number_of_results` | integer | No | Limit results (default 20) |
| `exclude_sponsored` | boolean | No | Remove sponsored results |
| `page` | integer | No | Results page number |

Response:

```json
{
  "success": true,
  "results": [
    {
      "position": 1,
      "asin": "B09F5RKG8P",
      "title": "Sony WF-C500 Wireless Earbuds",
      "price": { "value": 38.00, "currency": "USD", "raw": "$38.00" },
      "rating": 4.5,
      "ratingsTotal": 12420,
      "image": "https://m.media-amazon.com/...",
      "isPrime": true,
      "isBestseller": false,
      "isDeal": false,
      "isSponsored": false,
      "link": "https://amazon.com/dp/B09F5RKG8P"
    }
  ],
  "pagination": { "currentPage": 1, "totalPages": 20, "totalResults": 400 },
  "searchTerm": "wireless earbuds"
}
```

Show at least 3-5 results so the user can compare. The `isPrime` flag usually means free shipping.

## Step 2: Check Product Details

`/buy-amazon-details`

```bash
curl "{{BASE_URL}}/product/B09F5RKG8P"
```

Response:

```json
{
  "success": true,
  "product": {
    "asin": "B09F5RKG8P",
    "title": "Sony WF-C500 Wireless Earbuds",
    "description": "True wireless earbuds with...",
    "brand": "Sony",
    "price": { "value": 38.00, "currency": "USD", "raw": "$38.00" },
    "buyboxWinner": {
      "price": { "value": 38.00, "currency": "USD", "raw": "$38.00" },
      "shipping": { "value": null, "raw": "FREE" },
      "isPrime": true,
      "fulfillment": "1p",
      "availability": "In Stock"
    },
    "rating": 4.5,
    "ratingsTotal": 12420,
    "ratingBreakdown": { "5": 68, "4": 20, "3": 8, "2": 2, "1": 2 },
    "mainImage": "https://m.media-amazon.com/...",
    "specifications": [
      { "name": "Battery Life", "value": "8 hours" }
    ],
    "variants": [
      { "asin": "B09F5RKG8P", "title": "Black", "isCurrent": true },
      { "asin": "B0CKFBWVPL", "title": "White", "isCurrent": false }
    ]
  }
}
```

Check `buyboxWinner.shipping` — if it says "FREE", your user saves on shipping. Show the `ratingBreakdown` so users can gauge quality. If variants exist in different colors/sizes, let the user pick before adding to cart.

## Step 3: Add to Cart

`/buy-amazon-cart`

```bash
curl -X POST {{BASE_URL}}/cart \
  -H "Content-Type: application/json" \
  -d '{"asin": "B09F5RKG8P", "quantity": 1}'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `asin` | string | Yes | Amazon product ID from search/product results |
| `quantity` | integer | No | Number of items (default: 1) |

Response:

```json
{
  "success": true,
  "cartId": "cart_abc123",
  "items": [
    { "asin": "B09F5RKG8P", "title": "Sony WF-C500 Wireless Earbuds", "price": 38.00, "quantity": 1, "image": "https://..." }
  ],
  "subtotal": 38.00,
  "status": "OPEN"
}
```

Save the `cartId` — you need it for checkout and confirmation.

## Step 4: Checkout with Shipping Address

`/buy-amazon-checkout`

```bash
curl -X POST {{BASE_URL}}/cart/cart_abc123/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "shipping": {
      "name": "John Doe",
      "line1": "123 Main St",
      "line2": "Apt 4B",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105",
      "country": "US"
    },
    "agentId": "your-agent-id"
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `shipping.name` | string | Yes | Recipient full name |
| `shipping.line1` | string | Yes | Street address |
| `shipping.line2` | string | No | Apartment, suite, unit |
| `shipping.city` | string | Yes | City |
| `shipping.state` | string | Yes | 2-letter state code (e.g. "CA") |
| `shipping.zip` | string | Yes | ZIP code (5+ digits) |
| `shipping.country` | string | No | Country code (default: "US") |
| `agentId` | string | No | Your agent identifier for order tracking |

Response:

```json
{
  "success": true,
  "cartId": "cart_abc123",
  "summary": {
    "items": [{ "asin": "B09F5RKG8P", "title": "Sony WF-C500 Wireless Earbuds", "price": 38.00, "quantity": 1 }],
    "subtotal": 38.00,
    "shipping": 5.99,
    "serviceFee": 4.40,
    "total": 48.39
  },
  "shippingAddress": {
    "name": "John Doe",
    "line1": "123 Main St",
    "line2": "Apt 4B",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94105",
    "country": "US"
  },
  "message": "Review your order and confirm to place it."
}
```

**Always present this breakdown to the user before confirming:**
- Subtotal: product price
- Shipping: from Amazon (often FREE with Prime)
- Service fee: 10% of (subtotal + shipping)
- Total: what they'll pay

## Step 5: Confirm Order

`/buy-amazon-confirm`

```bash
curl -X POST {{BASE_URL}}/cart/cart_abc123/confirm
```

Response:

```json
{
  "success": true,
  "orderId": "AC-MLLZVLMB-001",
  "status": "PENDING_FULFILLMENT",
  "items": [{ "asin": "B09F5RKG8P", "title": "Sony WF-C500 Wireless Earbuds", "price": 38.00, "quantity": 1 }],
  "total": 48.39,
  "shippingAddress": { "name": "John Doe", "line1": "123 Main St", "city": "San Francisco", "state": "CA", "zip": "94105", "country": "US" },
  "message": "Order confirmed! We'll process it within 24-48 hours."
}
```

Save the `orderId` to track status later. The order will be fulfilled within 24-48 hours.

## Step 6: Track Order

`/buy-amazon-status`

```bash
curl "{{BASE_URL}}/order/AC-MLLZVLMB-001"
```

Response:

```json
{
  "success": true,
  "order": {
    "orderId": "AC-MLLZVLMB-001",
    "status": "PENDING_FULFILLMENT",
    "items": [{ "asin": "B09F5RKG8P", "title": "Sony WF-C500 Wireless Earbuds", "price": 38.00, "quantity": 1 }],
    "total": 48.39,
    "trackingNumber": null,
    "createdAt": "2026-02-14T07:28:09Z"
  }
}
```

**Order statuses:** `PENDING_FULFILLMENT` → `PROCESSING` → `SHIPPED` (tracking number added) → `DELIVERED`

To list all orders: `GET {{BASE_URL}}/orders`

## Example Conversation

```
User: Find me wireless earbuds under $50

Agent: Here are the top wireless earbuds under $50:

1. Sony WF-C500 - $38.00 ⭐4.5 (12,420 reviews) Prime
2. JBL Tune 130NC - $49.95 ⭐4.3 (8,200 reviews) Prime
3. Soundcore A20i - $29.99 ⭐4.4 (45,000 reviews) Prime

Want details on any of these?

User: The Sony ones look good. Buy them for me. Ship to John Doe, 123 Main St, San Francisco CA 94105

Agent: Here's your order summary:

  Sony WF-C500 Wireless Earbuds    $38.00
  Shipping                          $5.99
  Service fee (10%)                 $4.40
  ─────────────────────────────────
  Total                            $48.39

Ship to: John Doe, 123 Main St, San Francisco, CA 94105

Confirm order?

User: Yes

Agent: Order confirmed! 🎉

  Order #AC-MLLZVLMB-001
  Status: Processing
  Estimated fulfillment: 24-48 hours

I'll track this for you — just ask anytime.
```

## Quick Reference

```bash
# Search
GET {{BASE_URL}}/search?q=wireless+earbuds

# Product details
GET {{BASE_URL}}/product/B09F5RKG8P

# Create cart
POST {{BASE_URL}}/cart  {"asin":"B09F5RKG8P","quantity":1}

# Checkout
POST {{BASE_URL}}/cart/{cartId}/checkout  {"shipping":{"name":"...","line1":"...","city":"...","state":"CA","zip":"94105"}}

# Confirm
POST {{BASE_URL}}/cart/{cartId}/confirm

# Track order
GET {{BASE_URL}}/order/{orderId}

# List all orders
GET {{BASE_URL}}/orders
```
