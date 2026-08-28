# EXPLAIN Reading

Read plans as evidence.

## Estimated vs Actual
Large row-estimate errors can produce bad join/scan choices.

## Loops
A node taking 1 ms but executed 500,000 times can dominate the request.

## Scan Type
Sequential scan is not inherently bad; index scan is not inherently good.

## Join Type
Interpret nested loop/hash/merge from input sizes, cardinality, and cost rather than memorized rules.

## Buffers
When available, buffer data helps distinguish cache/I/O-heavy behavior and understand where work is happening.

## Rule
Find the node or pattern dominating actual work rather than optimizing the most visually complicated node.
