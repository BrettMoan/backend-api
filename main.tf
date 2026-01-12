
data "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
}

resource "aws_lambda_function" "fastapi" {
  filename         = "backend_api.zip"
  function_name    = "fastapi-serverless-api"
  role             = data.aws_iam_role.lambda_exec.arn
  handler          = "backend_api.handler.handler"
  runtime          = "python3.11"
  source_code_hash = filebase64sha256("backend_api.zip")
  timeout          = 30
  environment {
    variables = {}
  }
}
resource "aws_apigatewayv2_api" "fastapi" {
  name          = "fastapi-serverless-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "fastapi" {
  api_id                 = aws_apigatewayv2_api.fastapi.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.fastapi.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "fastapi" {
  api_id    = aws_apigatewayv2_api.fastapi.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.fastapi.id}"
}

resource "aws_apigatewayv2_stage" "fastapi" {
  api_id      = aws_apigatewayv2_api.fastapi.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fastapi.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.fastapi.execution_arn}/*/*"
}
