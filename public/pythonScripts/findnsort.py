import csv
import pandas as pd
import sys

def getDocArray(index):
    df= pd.read_csv("hello.csv")
    # df= df.values
    # print(type(df))
    # print(df)
    # print(ind)
    # df = ind.iloc[:,[index]] # Select columns by Index
    # print(df)
    selected_columns = df.iloc[:, [0, index]]
    # selected_columns = selected_columns.drop([0])
    # selected_columns = ind.iloc[1:, [0, index]]
    # print(selected_columns)
    pairs = list(zip(selected_columns[df.columns[0]], selected_columns[df.columns[index]]))
    # # Print the pairs
    # print(pairs)
    # selected_columns = selected_columns.sort_values(by=df.columns[index], ascending=False)
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
    # print(pairs)
    res_docs = []
    for pair in pairs:
        if(pair[1]>0):
            res_docs.append(pair[0])
    return res_docs

index = sys.argv[1]
index = index[1:-3]
# print(index, type(index))
ind = int(index)
# if ind == -1:
#     print("")
# print(ind, type(ind))
ans = getDocArray(ind)

with open('results.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Heading"])
    for doc_id in ans:
        writer.writerow([doc_id])

print("Results obtained : ", ans)