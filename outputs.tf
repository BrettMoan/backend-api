# Define outputs here
output "api_gateway_url" {
  description = "The invoke URL of the API Gateway HTTP API."
  value       = aws_apigatewayv2_api.fastapi.api_endpoint
}