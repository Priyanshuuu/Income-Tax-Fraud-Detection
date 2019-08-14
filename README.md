# Income-Tax Fraud Detection

## Description
* In many scenarios, tax payers must declare the amount according to the tax base in some process and pay a percentage of that amount.
* This implies that many tax payers under-report earnings to reduce their taxes, as they have no incentive to report the actual amount.
* What this project contains a web-app based api that uses *Unsupervised methodology* to detect and score tax payers under-reporting their tax base in order to pay less taxes than they should.

## Work Flow
1. First, a clustering phase is made, grouping similar tax declarations according to the values of their features.
2. Second, we adjust a probability distribution to the tax bases reported in each cluster.
3. Finally, we detect suspicious declarations using a quantile of the adjusted distribution.

## Technology Stack
**Python is the language of choice for this software because of its ease of use and extensive ecosystem of libraries in the field machine learning**
The language I am going to use :
* Sci-kit learn: For implementation of Supervised and Unsupervised learning algorithms (like Decision Trees, k-Means, Gaussian mixture model, Bayesian Gaussian model).
* Pandas: For analysis and managing of data.
* Matplotlib:
* Numpy:


