Title: Brick by Brick 2024
Date: 2025-02-01 00:00
Authors: me
Summary: Automating Building Data Classification
Template: project_detail
save_as: projects/brick-by-brick.html
Technologies:python,scikit-learn
Images:projects\brick.png
repository:https://github.com/tartieret/BrickToBrick

## Project description

My colleague Hatef Rahmani and I took part to the [Brick to Brick 2024 challenge organized on AI Crowd by UNSW Sydney](https://www.aicrowd.com/challenges/brick-by-brick-2024). The goal of the challenge was to classify building data streams into categories defined by the Brick schema. Using time-series data, including sensor readings and equipment statuses, we had to organize and standardize this information to streamline management processes. 

This was a challenging task due to the number of classes and time-series. You can find the full code and documentation [in the GitHub repository](https://github.com/tartieret/BrickToBrick), and a engineering report is available [here]().

In spite of limited time available, we ranked 8th out of 31 teams. The project was a great opportunity to apply machine learning techniques to a real-world problem in the building management domain. It also allowed us to deepen our knowledge of time-series data processing and classification algorithms.

We experimented with modern libraries such as [AutoGluon](https://auto.gluon.ai/), [Optuna](https://github.com/optuna/optuna) (for hyperparameter optimization), [TSFresh](https://tsfresh.readthedocs.io/en/latest/) (for time-series feature extraction), more classic libraries such as Scikit-learn and XGBoost, and mlflow for model tracking and management. I used also [Coiled](https://coiled.io/) for distributed training on a cluster of virtual machines in Azure.