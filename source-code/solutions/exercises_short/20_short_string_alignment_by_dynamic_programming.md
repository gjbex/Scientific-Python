# 20. Short string alignment by dynamic programming

## Example solution

Take the strings `CAT` and `CUT`, with match score `+1`, mismatch score `-1`, and gap penalty `-1`.

One optimal alignment is

```text
C A T
C U T
```

The score is

```text
+1  -1  +1  = 1
```

Because the strings have the same length and only one mismatch, no gap is needed.

## Minimal dynamic-programming table

```text
      -  C  U  T
   -  0 -1 -2 -3
   C -1  1  0 -1
   A -2  0  0 -1
   T -3 -1 -1  1
```

## Discussion

Backtracking from the bottom-right corner recovers the alignment above.
