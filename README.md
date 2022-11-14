# Naive-GE15-Prediction

##Overview
This simple web app aim to illustrate the potential outcomes of the upcoming GE15 by allowing users to change some assumption.
The main point is to demostrate how with Undi 18, young voters can have a significant impact on the elections given how close the field is.

### Assumption
The approach used is naive and take the following assumptions:
1) Voters prefers towards a party does not change over time(from GE13 - GE15). The only thing that's changing is the composition of the coalitions
2) By simply looking at the votes lost by BN/PAS in GE14, we can calculate the contribution of Bersatu and Amanah to the PH coalition
3) We ignore the votes won by independent parties assuming the majority of them do not have a sizeable amount

### Approach
The approach is as follows:
1) We will only be looking at the 165 constituencies in Peninsular Malaysia as assumption 3 does not hold well for most cases in East Malaysia
2) We normalise the number of voters to the total from GE13 and calculate Bersatu's contribution
3) The predict the outcome of GE15 by assuming BN hold the same number of supporters, Bersatu's contribution is added to PAS and PH is the diffrence of `GE14 - Bersatu`

### Parameters
The allows so free parameters to exist:
1) The contribution of Bersatu of BN's loss in GE14. In the base case we assume 100% of votes lost by BN set to Bersatu but this parameter can be changed
