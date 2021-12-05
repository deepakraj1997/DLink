
# importing the required module
import matplotlib.pyplot as plt
 
# x axis values
x = [10,50,100,500,1000,1500]
# corresponding y axis values
y = [150,300,740,3050,6300,7680]
 
# plotting the points
plt.plot(x, y, label = "K8s")

x1 = [10,50,100,500,1000,1500]
# corresponding y axis values
y1 = [270,520,850,4920,12410,17470]
 
# plotting the points
plt.plot(x1, y1, label = "single server")

# naming the x axis
plt.xlabel('Requests in parallel')
# naming the y axis
plt.ylabel('T (ms)')
 
plt.legend()
# giving a title to my graph
plt.title('Performance Comparision')
 


# function to show the plot
plt.show()