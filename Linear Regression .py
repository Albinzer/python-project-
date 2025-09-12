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

# Step 5: Make predictions for dataset
df["Predicted_Weight"] = model.predict(X)
print(df)

# Step 6: Plot the regression line
plt.scatter(X, y, color="blue", label="Actual Weight")
plt.plot(X, df["Predicted_Weight"], color="red", label="Regression Line")
plt.xlabel("Height (cm)")
plt.ylabel("Weight (kg)")
plt.title("Linear Regression: Weight vs Height")
plt.legend()
plt.show()

# Step 7: User input for new height
new_height = float(input("Enter a height in cm: "))   # user types a value
predicted_weight = model.predict([[new_height]])

print(f"Predicted weight for height {new_height:.1f} cm: {predicted_weight[0]:.2f} kg")
