# Force and Moments Transformation Tool - User Manual
1. input proper csv path for csv file containing force and moment and lcs data in env file, in proper format, as specified.
2. run code lcs_transform to get output vectors in lsc format.



# Force and Moments Transformation Tool - Requirements  

## 1. Introduction

### 1.1 Purpose
This software converts force and moment vectors on a 3D plate from the Global Coordinate System(GCS) to a Local Coordinate System(LCS). It also computes maximum force and momentum vector at each node in the LCS. The purpose is to allow engineers to analyze the effects of forces and momentum in LCS.

### 1.2 Scope
This application will
- Accept a csv file containing data of force and momentum vectors in GCS
- Accept an LCS definition document containing 
  - origin coordinates
  - two orientation vectors

### 1.3 Intended Audience
- Engineers
- Researchers studying stress
- Testers

### 1.4 Definitions and Acronyms used
- **GCS: Global Coordinate System**
The default Coordinate System where the origin is `(0,0,0)`

- **LCS: Local Coordinate System**
The user defined coordinate system where origin is not at `(0,0,0)`

- **Node**
Point where forces/moments are applied.
 
- **Moment**
Torque acting around a node.

## 2. Overall Description

### 2.1 Product Perspective
This is a standalone project that can be further integrated into simulation and development tools.

### 2.2 User Needs
- Input the structure's node force and moment data in GCS
- Input the local coordinate definition
- View the transformed coordinates along with the maximum force/momentum value 
- Ensure that the data is not changed during processing

### 2.3 Assumptions and Dependencies
**Assumtions:**
- input data would be properly formatted as per the given format 
- data would be consistent and not missing

**Dependencies:**
- input files
- python libraries:
  - *pandas*
  - <add other libraries>

## 3. Functional Requrirements
- Accept and Validate all GCS force/moment data
- Accept and validate LCS definition data
- Apply transformation to all force and moment vectors on all nodes
- Output printed in a proper readable format 


## 4. Non - Functional Requrirement
- **Accuracy**: Vector transformations must preserve vector magnitudes.
- **Usability**: Should accept inputs via csv file.
- **Maintainability**: Well-commented and modular code structure.
- **Documentation**: Properly documentated code for user's ease

## 5. System Design/Architecture

### 5.1 Data Flow
1. Input: Force and Torque vectors in GCS, and LCS definition
2. Procedure: Vector Translation and Change of Basis on input vecors
3. Output: Force and Torque vectors in LCS form along with maximum force values.


## 6. Appendix

## 6.1 Mathematical Equations used

###### Cross Product via Determinant (Plain Markdown)

Let A = (Ax, Ay, Az)  
Let B = (Bx, By, Bz)

The cross product **A × B** is given by the determinant:

|  i   |  j   |  k   |  
|:----:|:----:|:----:|  
| Ax   | Ay   | Az   |  
| Bx   | By   | Bz   |

Result:

A × B = i(Ay * Bz - Az * By)  
       − j(Ax * Bz - Az * Bx)  
       + k(Ax * By - Ay * Bx)


###### Vector Translation
Let:

- **v** = (vx, vy)  
- **t** = (tx, ty)

Then:

**v'** = (vx + tx, vy + ty)



###### Change of Basis Formula

Let:

- **v** be a vector in ℝⁿ
- **B** be a basis represented by column vectors: B = [b₁ b₂ ... bₙ]
- **[v]_B** be the coordinates of **v** in basis **B**

Then the relationship between the standard coordinates and the coordinates in basis **B** is:

**From Standard Coordinates to Basis B**
To convert **v** from standard coordinates to coordinates in basis **B**:

[v]_B = B⁻¹ · v

Where:
- `B⁻¹` is the inverse of the basis matrix `B`


