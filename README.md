# ManageYourTeams
Company website for teams management, stocks, production and performance

Divided into 5 users categories: Manager, Technicians, Workshop workers, Clients, Admin

Each user has its own workspace:

  - Technicians workspace:
    - Reporting tool : team leaders can report their employees work by selecting step by steps the scopes they worked on, affining the selectable choices for each technician. This way, the website can reduce the number of choices and errors, but also help reducing the time spent during the reporting due to the big amount of work done everyday.
    - Quality management : team leaders can specify if a new non-compliance ticket has been emmited by the client. They can also specify how went all the quality control checks during the production.
    - Performance Analysis : team leaders can monitor employees performance by recording the time to produce 1 item, and can report it in the database to help evaluate the performance in a right way
  
  - Workshop workspace:
    - Reporting tool : Employees working at the workshop can specify which packages they created today, allowing the technicians to know how many resources are available at the office to be picked up for refilling their stock on the production site.

  - Clients : Clients have an access to the progress on each project the company is running for them. They also have an access to the stocks levels on the production site, and can know in real time the company resources production rate (at the workshop)

  - A common workspace is dedicated to the inventory system, where any user can do an inventory for its working place (production or workshop)

  - Each employee report is ending by giving a feedback to allow them giving any other useful informations to their teammates, and they can assess (anonymously) their days using a rating system. 
    Thus, a mini Social Network is displayed on the homepage, allowing all the users to see the daily feedbacks of each user to improve inter/intra-sectorial communication

  - Manager: The Manager is provided a dashboard to see the global performance of the company.
    - Stocks in all places (workshop, production) and of all types
    - Non-compliance ticket follow up
    - Performance employees. Top 3 employees of the day/month/year. Bonus suggestion
    - Margins, net and gross
    - Wastes analysis (costs and numbers)
    - Employees satisfaction
    - Many filters for each of the features listed above (stats by scope, by employee, by period ect..)
    - Charts for all the features listed above
    - The manager can access to all the workspaces.

  - Admin:
    - The admin section helps to manage the database via an user-friendly interface.

This website has been built using Django
