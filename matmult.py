#Question 1

#This function multiplies each element in the matrix by a scalar value.
def mult_scalar(matrix, scale):
    #Initialize the resulting matrix.
    result = []
    #Temporary list to hold the multiplied values of each row.
    resultRow = []
    #Iterate over each row of the input matrix.
    for row in matrix:
        #Multiply each value in the row by the scalar and add to resultRow.
        for column in row:
            resultRow.append(column * scale)
        #Add the multiplied row to the result.
        result.append(resultRow)
        #Reset the resultRow for the next row.
        resultRow = []
    #Return the scaled matrix.
    return result

#The rows of the result matrix are determined by the number of rows on the left matrix
#And the columns of the result matrix are determined by the number of columns on the right matrix.
def mult_matrix(a, b):
    # Initialize an empty list to store the resulting matrix
    product_matrix = []
    
    # Get dimensions of the input matrices a and b
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])
    
    # Verify that the matrices can be multiplied
    if cols_a != rows_b:
        return "Invalid dimensions for matrix multiplication"
    
    # Compute the matrix product
    for i in range(rows_a):
        product_row = []
        for j in range(cols_b):
            sum_elements = 0
            for k in range(cols_a):
                sum_elements += a[i][k] * b[k][j]
            product_row.append(sum_elements)
        product_matrix.append(product_row)
    
    return product_matrix


#This function calculates the Euclidean distance between two points (rows in matrices).
def euclidean_dist(a,b):
	leftMatrx = a
	rightMatrix = b
	eachEuclideanValue = 0
	#Initialize the squared sum.
	finalEuclideanValue = 0

	#Loop through each dimension (column).
	for colIndex in range(len(a[0])):
		#Square the difference for the current dimension.
		eachEuclideanValue = (leftMatrx[0][colIndex] - rightMatrix[0][colIndex]) ** 2
		#Add to the squared sum.
		finalEuclideanValue += eachEuclideanValue

	#Take the square root of the squared sum.
	finalEuclideanValue = finalEuclideanValue ** 0.5
	#Return the Euclidean distance.
	return finalEuclideanValue