# SQL style guide

- Lowercase keywords, snake_case identifiers.
- Always alias joined tables with short names: `o` for orders, `oi` for order_items,
  `p` for products, `c` for customers.
- Revenue is `sum(oi.quantity * oi.unit_price)` and excludes orders with status
  cancelled or returned.
- Prefer aggregates with a `limit` over raw row dumps.
- Date filters use ISO strings, for example `where o.order_date >= '2025-01-01'`.
