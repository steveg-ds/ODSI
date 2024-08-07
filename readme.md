# ODSI

This repository contains a set of web applications designed to tabulate debate tournaments and provide an online interface for collecting ballots. It is currently known as ODSI: The (Unofficial) Official Debate Software of the IPDA. My goal is to deliver an all-in-one system for running debate tournaments, specifically tailored for the International Public Debate Association (IPDA). The design incorporates feedback from coaches, past and present competitors, and several authors of the organization's constitution and founding members.

Features

Tournament Web Application

The "Tournament" web application offers tournament tabulation staff all necessary functionalities to pair debaters for both preliminary and elimination rounds. It addresses several problems noted by the community with existing systems:

Enhanced Pairing Algorithm: It eliminates the rigidity of traditional bracket systems that require extensive hard coding and are often unsuitable for smaller tournaments (fewer than 12-14 debaters). Our system checks all possible pairs and calculates the maximum number of valid preliminary rounds, avoiding issues inherent in traditional bracket structures.

Automated Advancement Calculations: The application automates the calculation of the number of advancing debaters in each division, significantly reducing the potential for human error.

Note: Eventually, the tournament selection dropdown bar will be replaced with a sign-in prompt, linking users directly to their tournaments.

Judging Web Application

The "Judging" web application introduces the first integrated online ballot system specifically designed for the IPDA, offering several key benefits over current systems:

Improved Accessibility: Using a framework that adjusts automatically to screen size, the application supports use in mobile browsers, which is not possible with current systems. This enhances accessibility, reducing the need for laptops and making the system usable by the 90% of U.S. adults who own a smartphone.

Enhanced Feedback System: The application reintroduces the speaker point feedback system, abandoned due to high rates of human error in calculating speaker points. Judges rank each speaker across various categories, and the final speaker point score is automatically calculated.

Streamlined User Experience: Unlike the most popular current systems for online ballots, there is no need for users to navigate to their ballot. All necessary information is automatically populated upon login.

Structured Data Collection: Data collected from ballots are well-structured for use in text processing applications, offering coaches and debaters detailed insights quickly. In the long term, this data will be an invaluable resource for coaches, competitors, and communications scholars.

Email Functionality: Although the current implementation is very limited, the core functionality to send judges emails informing them that they have recieved a ballot is there.

Data Storage and Deployment

All data are stored in a MongoDB database. The web applications and database will run in a multi-container Docker application using Nginx and Gunicorn to serve the Flask server on which the Dash app is built.

Cost Reduction through Self-Hosting One of the significant advantages of ODSI is its ability to be self-hosted, which can substantially reduce costs associated with running debate tournaments. By self-hosting, organizations can avoid expensive subscription fees for third-party services and maintain greater control over their data.

Cost Efficiency: Due to the small number of users the application needs to support at one time- a maximum of 150 concurrent users on the Judging app and maybe 10 concurrent users on the Tournament app, I intend to self-host everything securely rather than turning to the cloud. This reduces the cost of hosting a tournament significantly which may open the door for student-run teams or teams with little/ no budget to be able to host a tournament for the first time which would provide them with the opportunity to bring in a significant amount of money at a low cost.

Future Development

I have deemed this version 0.1 for a reason. Some features, such as power matching/ power protecting, are still under development. However, it is close to being ready for testing at a smaller tournament where power matching is not required. Once I can collect real world user feedback I will focus much more on improving the functionality and making the UI less plain. There is still a long ways to go but I am committed to making collegiate debate a more accessible activity.