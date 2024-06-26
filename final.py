import streamlit as st
from sklearn import datasets
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# Set page configuration and custom CSS for background color
st.set_page_config(page_title="Breast Cancer Dataset Analysis", page_icon="🎗️")
custom_css = f"""
    <style>
        body {{
            background-color: #FFD1DC; /* Breast cancer pink color code */
        }}
        .stApp {{
            background-color: #FFD1DC; /* Apply to entire app container */
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Display title and image
st.title("🎗️ Breast Cancer Dataset Exploration and Classification")
# st.image("data/BreastCancerRibbonEmoji.png", width=120)

# Display app description
st.markdown("""
Welcome to the Breast Cancer Dataset Analysis and Classification App! This interactive tool provides insights into the characteristics of breast tumors using advanced data visualization and machine learning techniques. Leveraging the renowned Breast Cancer dataset from Scikit-learn, this app empowers you to explore, visualize, and predict tumor classifications with ease.
<!-- Add a horizontal line -->
<small><em>Please note: This app is for educational purposes only. Do not use this app for self-diagnosis or medical decision-making.</em></small>
""", unsafe_allow_html=True)

st.write("### How to Use")

# Data Exploration
st.write("#### Click on data exploration tab to:")
st.write("- Investigate the dataset's characteristics, including sample size, feature dimensions, and available classes.")

st.write("#### Click on data visualization tab to:")
st.write("- View correlation patterns using the heatmap to identify significant relationships between features.")
st.write("- Customize pair plots to examine feature interactions and distributions.")
st.write("- Choose feature pairs interactively to visualize and analyze potential patterns.")

# Decision Tree Visualization
st.write("#### Click on Classification Model tab to:")
st.write("- Explore decision tree diagrams to understand the underlying structure of classification models.")
st.write("- Gain insights into feature importance and decision-making processes.")

# Load breast cancer dataset
breastCancer = datasets.load_breast_cancer()
df = pd.DataFrame(breastCancer.data, columns=breastCancer.feature_names)
df['target'] = breastCancer.target

# Display horizontal tabs for navigation
tabs = ["Data Exploration", "Data Visualization", "Classification Model"]
selected_tab = st.selectbox("Explore options", tabs)

# Define functions for Data Exploration and Model Training
def data_exploration():

    st.header("Data Exploration")
    
    # Description of data exploration
    st.markdown("""
    Explore the characteristics of the breast cancer dataset, including sample statistics, feature dimensions,
    and available classes. This section provides an overview of the dataset's key attributes.
    """)

    # Display sample statistics
    st.write("Number of samples:", df.shape[0])
    st.write("Number of features:", df.shape[1])
    st.subheader("Classes:")
    st.write(", ".join(breastCancer.target_names))

    # Display sample data
    st.subheader("Sample Data:")
    st.write(df.head(7))

def data_visualization():
    # Display correlation heatmap using Seaborn and Matplotlib
    st.write("### Correlation Heatmap")
    st.write("Correlation is a statistical metric that quantifies the association between two variables, ranging from -1 to 1. A positive correlation signifies a direct relationship, whereas a negative correlation indicates an inverse relationship. ")
    corr_matrix = df.corr()
    threshold = st.slider("Select Correlation Threshold", min_value=0.0, max_value=1.0, value=0.75, step=0.01)
    filtre = np.abs(corr_matrix["target"]) > threshold
    corr_features = corr_matrix.columns[filtre].tolist()

    plt.figure(figsize=(14, 12))
    sns.heatmap(df[corr_features].corr(), linewidths=0.1, square=True, linecolor='white', annot=True)
    heatmap_fig = plt.gcf()  # Get current figure
    st.write(f"### Correlation Heatmap (Threshold: {threshold})")
    st.pyplot(heatmap_fig)  # Display the heatmap figure

    # Generate pairplot for selected features with customized settings
    st.write("""
    ## Pair Plot Analysis with KDE Diagonals
    
    Pair plots with KDE diagonals provide an insightful visualization of feature interactions and distributions within the breast cancer dataset. Each scatterplot in the pair plot matrix displays the relationship between two different features, allowing for the identification of potential patterns and correlations.
    
    **Interactive Feature Selection**
    
    This pair plot analysis is interactive, allowing you to choose specific feature pairs to visualize and analyze. By selecting feature pairs dynamically, you can gain deeper insights into how different features interact and influence tumor classification.
    
    **Target Variable (Outcome)**
    
    The pair plots include the target variable (tumor classification) as a hue parameter. This hue parameter colors the scatterplot points based on the target variable, enabling visual differentiation between benign and malignant tumors. Through this visualization, you can observe how feature combinations relate to tumor classification outcomes.
    """)
    feature_names = breastCancer.feature_names
    df['target'] = breastCancer.target
    # Select pairs of features for pair plot using Streamlit multiselect widget
    selected_pairs = st.multiselect("Select Feature Pairs", options=feature_names, default=feature_names[:4])

    if len(selected_pairs) > 4:
        st.warning("Please select a maximum of 4 feature pairs.")
        selected_pairs = selected_pairs[:4]  # Limit selection to first 8 features


    # Filter DataFrame to include selected feature pairs
    selected_df = df[selected_pairs + ['target']]

    # Pair plot based on selected feature pairs
    if selected_pairs:
        st.write(f"Pair Plot for Selected Feature Pairs: {', '.join(selected_pairs)}")
        pairplot = sns.pairplot(selected_df, hue='target')
        st.pyplot(pairplot)
    else:
        st.write("Please select feature pairs to display the pair plot.")


def classification_model():
    X = breastCancer.data
    y = breastCancer.target
    # Create DataFrame from features
    df = pd.DataFrame(X, columns=breastCancer.feature_names)

    # Streamlit app layout
    st.title("Breast Cancer Diagnosis - Decision Tree Analysis")

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train Decision Tree classifier
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Make predictions on test data
    y_pred = clf.predict(X_test)

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Display model evaluation metrics
   
    st.write("""
    ## Model Evaluation Metrics
    
    Model evaluation metrics assess the performance of our classification model on the breast cancer dataset. Common metrics include accuracy, precision, recall, F1-score, and area under the ROC curve (AUC-ROC). These metrics provide a comprehensive view of a model's effectiveness in distinguishing between benign and malignant tumors, considering both predictive accuracy and class imbalance.
    """)
    
    st.write(f"Accuracy: {accuracy:.4f}")
    st.write(f"Precision: {precision:.4f}")
    st.write(f"Recall: {recall:.4f}")
    st.write(f"F1-score: {f1:.4f}")

    # Confusion Matrix
    
    st.write("""
    ## Confusion Matrix
    
    A confusion matrix is a table that summarizes the performance of a classification model. It presents the predicted classifications of a model against the actual classifications in a tabular format. The matrix provides insights into the model's ability to correctly or incorrectly classify instances, distinguishing between true positives, true negatives, false positives, and false negatives.
    """)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='cividis', cbar=False)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    st.pyplot()

    # Decision Tree Diagram
    
    st.write("""
    ## Decision Tree Diagram
    
    A decision tree diagram visually represents the structure of a decision tree model used for classification. Each node in the tree represents a decision based on a feature, leading to subsequent nodes or leaves that correspond to predicted class labels. Decision trees are powerful tools for understanding the logic behind classification decisions and identifying important features for prediction.
    """)
   
    fig, ax = plt.subplots(figsize=(20, 10))  # Create a Matplotlib figure and axis
    plot_tree(clf, feature_names=breastCancer.feature_names, filled=True, fontsize=8, ax=ax)  # Plot decision tree
    st.pyplot(fig)  # Display the figure in Streamlit
    


    # Feature Importance
    
    st.write("""
    ## Feature Importance
    
    Feature importance quantifies the contribution of each feature in a machine learning model towards making accurate predictions. For classification tasks, feature importance scores highlight which features are most influential in determining class labels. Understanding feature importance aids in feature selection, model interpretation, and identifying key factors driving classification outcomes.
    """)
    
    feature_importance = clf.feature_importances_
    sorted_idx = np.argsort(feature_importance)
    top_features = df.columns[sorted_idx][-10:]  # Select top 10 important features
    plt.figure(figsize=(10, 6))
    plt.barh(top_features, feature_importance[sorted_idx][-10:])
    plt.xlabel("Feature Importance")
    plt.title("Top 10 Important Features")
    st.pyplot()



# Render content based on selected tab
if selected_tab == "Data Exploration":
    data_exploration()
elif selected_tab == "Data Visualization":
    data_visualization()
elif selected_tab == "Classification Model":
    classification_model()
