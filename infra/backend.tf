# terraform {
#   backend "gcs" {
#     bucket  = "my-terraform-state-bucket"
#     prefix  = "deepseek-r1/terraform"
#   }
# }

# Using GCS backend now that billing is enabled
terraform {
  backend "gcs" {
    bucket  = "deepseek-terraform-state"
    prefix  = "deepseek-r1/terraform"
  }
}