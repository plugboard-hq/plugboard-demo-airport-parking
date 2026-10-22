# Data dictionary: sales warehouse

All tables live in the single SQLite file `data/demo.sqlite`.

## customers
One row per customer. `region` is one of North, South, East, West. `segment` is
`consumer` or `business`. `signup_date` is ISO formatted.

## products
One row per product. `category` is Coffee, Tea, Equipment or Accessories. `unit_price`
is the current list price.

## orders
One row per order. `status` is shipped, delivered, cancelled or returned. Revenue
reports should exclude cancelled and returned orders.

## order_items
One row per line on an order. `unit_price` is the price at the time of the order, which
may differ from the product's current list price. Line revenue is `quantity * unit_price`.

## inventory
One row per product with `on_hand` stock and a `reorder_point`. A product needs
reordering when `on_hand` is below `reorder_point`.
