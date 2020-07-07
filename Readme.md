# Predicting Recession in US 

The overview of the project is to build a data analytic and predictive platform to visualize the inference and recession in US for 6month,
12month and 24month based on the economic and market data. The main economic features are used in the project are:
* **Total Nonfarm Payrolls**: - The measure of the number of US workers in the economy. When Businesses
are slow, the pace of hiring becomes slow in the challenging economic environment. The percentage
change 3 months and 12-month Nonfarm Payrolls is used as the best predictor variable.
* **Effective Federal Funds Rate**:- the federal funds rate is the interest rate at which banks and credit
unions lend assets balances to other depository institutions overnight on an uncollateralized basis. I have
calculated the 12-month change ineffective federal funds Rate and added feature list.
* **Consumer Price Index**: it is a measure of weighted average prices for consumer goods and services.
The consumer price index acts as a proxy for inflation. Inflation is a factor for economic challenges and
triggers Recession.
* **Treasury Rate**: It is the current interest rate investors earn on government bonds and bills issued by the
US treasury. The yield curve is calculated by the spread between 3 month and 10-year treasury bills.
The inverted yield curve is a consistent indicator of recession ([Winck 2019](https://www.businessinsider.com.au/yield-curve-inversion-explained-what-it-is-what-it-means-2019-8?r=US&IR=T))
* **Market Data**: The last feature is the stock market data of 500 large companies listed on the US stock
exchanges. I have used yahoo finance to collected the S&P500 data.
#### **Use of the Project**
* It helps the policymakers to take countermeasures to decrease the impact of the Recession. The
prediction helps to stimulate the economic conditions.
* Tackling the problems helps the investors to save money by implementing defensive investment
strategies
#### **Architecture**
The data analytic and predictive platform built using Flask API and a static web dashboard. The Flask web API used for data collection and real-time data visualization. The real-time data collected using [FRED API](https://fred.stlouisfed.org/docs/api/fred/) further undergo exploratory data analysis and feed into the machine learning pipeline. The real-time visualization rendered using chartjs and vuejs. 

* Developed a website dashboard using bootstrap, Vuejs, and CSS. The website is hosted on a Ubuntu server, secured the request using lets-encrypt SSL certificate. Created an apache configuration for routing the flask web server. 
  * https://companyandngo.xyz/ 
  * https://api.companyandngo.xyz/
* Real time visualization. The parameters are passed to the API to fetch economic data.
   * https://api.companyandngo.xyz/graph?id=yahoo
```javascript
function chart (name, label, element, type){
                this.loading = true
                //url = 'http://localhost:5000/graph'
                 url ='https://api.companyandngo.xyz/graph'
                axios.get(url, {
                    params: {
                        id: name
                    }
                }).then(response => {
                        res = response.data
                        var ctx = document.getElementById(element);
                        var dates = res[name][0].map(list => {
                            return moment(list, 'YYYY-MM-DD').toDate()
                        });
                        var value = res[name][1]
                        var annotations = recession_data.map((date, index) => {
                            return {
                                type: 'box',
                                xScaleID: 'x-axis-0',
                                yScaleID: 'y-axis-0',
                                xMin: date.start_date,
                                xMax: date.end_date,
                                yMin: type,
                                yMax: Math.max.apply(Math, value),
                                backgroundColor: 'rgba(101, 33, 171, 0.5)',
                                borderColor: 'rgb(101, 33, 171)',
                                borderWidth: 1,
                            }
                        });
                        this.chart = new Chart(ctx, f(dates, annotations, value, label));
                    }
                ).catch(error => {
                    console.log(error);
                    this.errored = true;
                }).finally(() => {
                    this.loading = false
                })}
```
* The economic impact of the COVID-19 on stock market 
![Yahoo stock](https://i.ibb.co/0fJdXJb/image.png)
 * The graph shows the live adjusted closing of stock and how the market value changing due to pandemic.

#### **Model Selection**
![](https://i.ibb.co/LzKHt32/j.png)
* Data split and Adaptive Synthetic Method to perform minority class oversampling

![](https://i.ibb.co/gTtjMnP/image.png)
* Determine ideal hyper parameters for each model for recession to maximize ROC_ AUC curve to evaluate each model and identify best model to be used.

![](https://i.ibb.co/0YY56GQ/image.png)
* Selecting the best model based on ROC validation score so Logistic regression to predict recession probabilities

#### **Recession Models**

6 month Recession

|Classifier Name|Best Tuning Parameter|Train ROC_AUC|Test ROC_AUC|
|--- |--- |--- |--- |
|XGBClassifier|{colsample_bytree: 0.9, gamma: 0.0, max_depth: 8, reg_alpha: 0.005}|0.960555|0.426709|
|KNeighbors Classifier|{n_neighbors: 2}|0.939149|0.412904|
|Logistic Regression|{C: 1000.0, penalty: l2}|0.880414|0.430584|
|Support Vector Machine|{C: 1000, gamma: 0.001, kernel: rbf}|0.875987|0.412149|

12 month Recession

|Classifier Name|Best Tuning Parameter|Train ROC_AUC|Test ROC_AUC|
|--- |--- |--- |--- |
|XGBClassifier|{colsample_bytree: 0.9, gamma: 0.2, max_depth: 9, reg_alpha: 0}|0.953282|0.607096|
|KNeighborsClassifier|{n_neighbors: 4}|0.942960|0.584423|
|Logistic Regression|{C: 1000.0, penalty: l2}|0.844857|0.619935|
|Support Vector Machine|{C: 1000, gamma: 0.001, kernel: rbf}|0.833734|0.603888|

24 month Recession

| Classifier Name                                         | Best Tuning Parameter                                              | Train ROC_AUC | Test ROC_AUC |
|---------------------------------------------------------|--------------------------------------------------------------------|---------------|--------------|
| XGBClassifier                                           | {colsample_bytree: 0.7, gamma: 0.0, max_depth: 9, reg_alpha: 0.05} | 0.942987      | 0.571329     |
| KNeighbors Classifier                                   | {n_neighbors: 3}                                                   | 0.919971      | 0.505878     |
| Support Vector Machine                                  | {C: 1000, gamma: 0.001, kernel: rbf}                               | 0.740931      | 0.602535     |
| Logistic Regression                                     | {C: 1000.0, penalty: l2}                                           | 0.718052      | 0.628138     |

### Prediction

![](https://i.ibb.co/s3H2gdD/image.png)
* The graph visualises the recession probabilities from 1960 to 2020. An increase in recession probabilities is followed by a recession, which is highlighted in the shaded area. A point to be noted is that, the recession probabilities as predicted by the model are increasing now and this can be considered as an indicator for a recession. Using the model built, the recession probabilities as of April 2020 are

|Date|Recession in 6month probability|Recession in 12month probability|Recession in 24month probability|
|--- |--- |--- |--- |
|2020-04-01|0.999973|0.843050|0.000421|
|2020-03-01|0.939977|0.120969|0.106055|
|2020-02-01|0.819899|0.393791|0.380028|



   




