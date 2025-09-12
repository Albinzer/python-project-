# Step 1: Import libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Step 2: Sample dataset
data = {
    "Height": [150, 160, 165, 170, 175],
    "Weight": [50, 55, 60, 65, 70]
}

df = pd.DataFrame(data)

# Step 3: Prepare X (independent) and y (dependent)
X = df[["Height"]]  # height is independent variable
y = df["Weight"]    # weight is dependent variable

# Step 4: Create Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Step 5: Make predictions
df["Predicted_Weight"] = model.predict(X)

# Step 6: Display results
print(df)

# Step 7: Plot the regression line
plt.scatter(X, y, color="blue", label="Actual Weight")
plt.plot(X, df["Predicted_Weight"], color="red", label="Regression Line")
plt.xlabel("Height (cm)")
plt.ylabel("Weight (kg)")
plt.title("Linear Regression: Weight vs Height")
plt.legend()
plt.show()
