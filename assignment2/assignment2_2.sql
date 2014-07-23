-- Problem 2g
SELECT val FROM (
	SELECT
		a.row_num AS row, 
		b.col_num AS col, 
		SUM(a.value * b.value) AS val
		FROM a, b
		WHERE
		a.col_num = b.row_num
		GROUP BY
		a.row_num, b.col_num
)
	WHERE 
	row = 2 AND col = 3;
	
SELECT val FROM (
	SELECT
		a.row_num AS row, 
		b.row_num AS col, 
		SUM(a.value * b.value) AS val
		FROM a, b
		WHERE
		a.col_num = b.col_num
		GROUP BY
		a.row_num, b.row_num
)
	WHERE 
	row = 0 AND col = 0;