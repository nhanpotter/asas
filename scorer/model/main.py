from .model import *
from .preprocess import *


def avg(rms, mae):
    return (rms + mae) / 2


def buildmodel(questions, answers):
    input_dataset = './Augmented_Feat.csv'
    embedmodel = train_word2vec(
        './glove.6B.300d.txt')
    question = './questions.csv'

    data = preprocess(questions, answers)
    df = cleaning_dataset(data, input_dataset)
    df = question_demoting(df, question, questions)

    X, y, scaler_y = scale(df)

    X_train, X_test, y_train, y_test = splittest(X, y, 0.2)

    print('==================== Training ====================')
    train_model, tokenizer = train_lstm(
        X_train, y_train, embedmodel)
    print('==================== Training done ====================')

    print('==================== Validation metrics ====================')
    test_results = predict(X_test, train_model, tokenizer)
    test_results, y_true = processresult(test_results, y_test, scaler_y)
    pearson, rmse, mae = evaluate(test_results, y_true)

    print("Pearson", round(pearson, 4))
    print("RMS", round(rmse, 4))
    print("MAE", round(mae, 4))

    metric = []
    metric.append({'metric': 'Pearson', 'value': pearson})
    metric.append({'metric': 'RMSE', 'value': rmse})
    metric.append({'metric': 'MAE', 'value': mae})

    return metric, train_model, tokenizer, data, scaler_y


def buildmodel_c(questions, answers):
    input_dataset = './Augmented_Feat.csv'
    embedmodel = train_word2vec(
        './glove.6B.300d.txt')
    question = './questions.csv'

    data = preprocess(questions, answers)
    df = cleaning_dataset(data, input_dataset)
    df = question_demoting(df, question, questions)

    X, y = scale_c(df)

    X_train, X_test, y_train, y_test = splittest(X, y, 0.2)

    print('==================== Training ====================')
    train_model, tokenizer = train_lstm_c(
        X_train, y_train, embedmodel)
    print('==================== Training done ====================')

    print('==================== Validation metrics ====================')
    test_results = predict_c(X_test, train_model, tokenizer)
    test_results, y_true = processresult_c(test_results, y_test)
    acc, report, f1 = evaluate_c(test_results, y_true)

    print('Accuracy', round(acc, 4))
    print('F1 score', round(f1, 4))
    print('Report')
    print(report)

    metric = []
    metric.append({'metric': 'Accuracy', 'value': acc})
    metric.append({'metric': 'F1 score', 'value': f1})

    return metric, train_model, tokenizer, data


def score(df_test, model, tokenizer, scaler_y):
    print('==================== Scoring ====================')
    test_results = predict(df_test, model, tokenizer)

    t = []
    for i in range(len(test_results)):
        temp = []
        temp.append(test_results[i])
        t.append(temp)
    test_results = t
    test_results = pd.DataFrame(test_results)
    test_results = scaler_y.inverse_transform(test_results)
    t = []
    for i in range(len(test_results)):
        for x in test_results[i]:
            t.append(x)
    test_results = t

    print('==================== Scoring done ====================')
    return test_results


def score_c(df_test, model, tokenizer):
    print('==================== Scoring ====================')
    test_results = predict_c(df_test, model, tokenizer)

    t = []
    for x in test_results:
        t.append(np.where(x == np.amax(x))[0][0])
    test_results = t

    print('==================== Scoring done ====================')
    return test_results
