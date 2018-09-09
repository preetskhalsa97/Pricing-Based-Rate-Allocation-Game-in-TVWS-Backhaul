# Pricing-Based-Rate-Allocation-Game-in-TVWS-Backhaul
Ghosh, Suman, Sandip Karar, and Abhirup Das Barman. <br>
"A Pricing-Based Rate Allocation Game in TVWS Backhaul and Access Link for Rural Broadband." <br>
IEEE Systems Journal 99 (2018): 1-8. <br>
<br>
Acknowledgement: <br>
Dr. Vinay Chamola (BITS Pilani) for the guidance <br>
Dr. Abhirup Das Barman for clarification on the paper<br>
<br>
NOTE: <br>
1. Formula 12 in the paper gives threshold prices in unit/bps and NOT in unit/Mbps, that might as well be the bottleneck in your implementation. <br>
2. You might never be able to match results to the final paper. You see (in table IV), their optimum solution dictates that the CPEs would be operating under a loss (CBS price < CPE price for all data restrictions) :P 
<br>
Running the simulation: <br>
run simulation.py (python-2.7)<br>
<br>
Output:<br>
Line1: x- axis values of all the particles initiated for finding optimal price offered by the CBS for a given k- value (change ki_array to find values for different k-values)<br>
Line2: respective utility value of the first particle at the end of all iterations (since convergence has been assumed)<br>
Line3: [[optimum prices for each CPE],[total data required for each CPE]]<br>