# Clinical Trials Study Design Prediction

This project fetches clinical trial data from the [ClinicalTrials.gov API](https://clinicaltrials.gov/api/gui), processes it, and stores it in a DynamoDB table. The goal is to build a model that predicts study design based on the fetched data.

## Project Structure
clinical-trials-project/
├── README.md # Project overview and documentation
├── lambda_function.py # AWS Lambda function code
├── infrastructure/ # Infrastructure-as-code files
│ ├── cloudformation.yaml # CloudFormation template for deployment
├── examples/ # Example requests and responses
│ ├── example-request.json
│ ├── example-response.json

License
This project is licensed under the MIT License. See the LICENSE file for details.

Copy

---

### **5. Next Steps**
- Model training, evaluation, and deployment
- Add **unit tests** for the Lambda function.
- Include **architecture diagrams** in the `docs/` folder.
- Use **CI/CD pipelines** (e.g., GitHub Actions) for automated deployment.
