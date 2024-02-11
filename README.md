# TIme varying Ankle Impedance

Conducted analysis of the inversion-eversion of ankle joint for the estimation of ankle impedance control required for a human 
rehabilitation system using an Anklebot robot.

Implementation and addition to the Paper : Time-Varying Ankle Mechanical Impedance During Human Locomotion


## Abstarct
This study uses data from the Anklebot wearable ankle robot to investigate ankle impedance during locomotion. Departing from traditional linear time-invariant models, we em-
ploy modified linear time-varying (LTV) ensemble-based system identification. Our focus extends beyond the steady state to capture time-varying characteristics throughout the gait cycle,specifically pre-swing through early stance.The model, mathematical equations, and results of this novel approach are discussed. The study contributes insights into
ankle rehabilitation by offering a dynamic understanding of ankle mechanics. The findings have implications for tailoring rehabilitation programs to specific gait phases. Future directions for research in biomechanics and rehabilitation are outlined


## Methodology
This method is based on the correlation approach, which assumes that every realization experiences the same underlying time-varying behaviour. By evaluating the input-output relation using data across realizations and time, the system dynamics can be identified at a specific time t
![Input Ankle Angle](https://github.com/YashasShetty/time_varying_ankle_impedance/assets/112819834/7ba95c0c-a438-4431-9913-7f40021df7f6)

![image1](https://github.com/YashasShetty/time_varying_ankle_impedance/assets/112819834/fb34c87f-2f78-49e7-83f2-1feeef3b2c83)


## Results
The mechanical impedance of an ankle was estimated using the ensemble technique. Inertia, viscosity, and stiffness were estimated for each time step. The plots for the same are shown below.
![IBK_plots](https://github.com/YashasShetty/time_varying_ankle_impedance/assets/112819834/0bb1fe75-2658-4613-bac6-6be93c8ef890)


## Conclusion
We were able to compute the impulse response function and estimate the ankle dynamics from it. As part of modifications, we evaluated the significance of the
Anklebot dynamics in the dynamics of the entire system which is obtained from the inputs and outputs. 


Collaborators
* **Yashas Shetty**<br>
[![LinkedIn](https://www.linkedin.com/in/yashas-shetty-046858168/) 
* **Sameer Arjun Satheesh**<br>
[![LinkedIn](https://www.linkedin.com/in/sameer-arjun-satheesh/) 
  
