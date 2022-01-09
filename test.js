const AWS = require("aws-sdk");

exports.handler = async (event) => {
    // TODO implement
    
    const dynamo = new AWS.DynamoDB.DocumentClient();
    let requestBody = event.body
  await dynamo.put(
                {
                    TableName: "piGPS_data",
                    Item: {
                        record: requestBody
                    }
                }
            )
    const response = {
        statusCode: 200,
        body: JSON.stringify(requestBody),
    };
    return response;
};

{
    "id\": \"1",
    "test\": \"abc1244"
}