from sklearn.datasets import fetch_openml

# Загрузка данных MNIST
mnist = fetch_openml('mnist_784', version=1)
X, y = mnist['data'], mnist['target']

from sklearn.model_selection import train_test_split

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import ExtraTreesClassifier

# Создание экземпляра классификатора Extra Trees
clf = ExtraTreesClassifier(n_estimators=100, random_state=42)

# Обучение классификатора на обучающих данных
clf.fit(X_train, y_train)

from sklearn.metrics import accuracy_score

# Предсказание меток для тестовых данных
y_pred = clf.predict(X_test)

# Оценка точности модели
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

from sklearn.metrics import confusion_matrix, classification_report

# Матрица ошибок
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Отчет о классификации
class_report = classification_report(y_test, y_pred)
print("\nClassification Report:")
print(class_report)

import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.pyplot as plt
import seaborn as sns

# Визуализация матрицы ошибок
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="YlGnBu", xticklabels=range(10), yticklabels=range(10))
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()


import joblib

# Сохранение модели
joblib.dump(clf, 'extra_trees_mnist_model.joblib')

# Загрузка модели (для проверки)
loaded_model = joblib.load('extra_trees_mnist_model.joblib')

# Проверка точности загруженной модели
loaded_model_accuracy = accuracy_score(y_test, loaded_model.predict(X_test))
print(f'Loaded Model Accuracy: {loaded_model_accuracy * 100:.2f}%')

