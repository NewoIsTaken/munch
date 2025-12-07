# Munch

## Background



## How we made it.

### In the beginning, there was Munch.
At the beginning of the process, we spent a long time brainstorming what we wanted to do. Over lunch, the picky eater in our group, Brian, pointed out how students never know how the food is like at Berg unless he tried it (and didn't like it) himself. From then, Munch was born.

### General Platform Ideation
Once we had a vague idea of what we wanted to do, we spent significant time drawing out exactly how we envision people interacting with our app. Knowing the natural laziness of us all, we knew we had to make the app as straightforward as possible to promote more usage of the app, else people would not go through the hassle. We held this value key throughout the rest of our design: something lightweight and quick that students would be able to quickly open, use, and the move on, perhaps during a meal or shortly after on their walk out.

While we could've made iOS/Android native applications, this would be much more complex and require multi-platform development to reach everyone with a mobile device. Additionally, this would require students to install yet another application on their phones that just adds to the massive amount of random apps we all have our phones nowadays. So, we decided to use a web application approach which allows us to design one application that is cross platform by nature.

### UI/UX Design
After firming up our target audicence and how they would interact with our application, we began design on the UI/UX of Munch. Given the design constraint of something simple and easy that held our users hand, we wanted to make the UI & UX as streamlined as possible with limited choices to make and one straightforward flow. With this in mind, we outlined our application both on Figma and whiteboard sketches, designing our home and rating pages. This is what lead to our very "app-like" and simple homepage who's main function is just find out what the user wants us to do. Additionally, our rating page is also a simple, straightforward star rating.

### Flask App Development
We've determined that we wanted to create a web app and we now knew what it would look like. Then, we had to go forward with creating the application. We were considering what platform to develop it on and we eventually selected Flask and Jinja due to our more familiarity with it in comparison to React. Thus, this application uses a very similar stack compared to the CS50 finance PSet.

Then, lots of coding was done.

## Future Improvements
Should we continue work on this project in the future, there are more features that we would add, listed in order of priority:
 - Implement HarvardKey login to ensure only Harvard Students/Affiliates can vote and prevent multiple votes by the same person.
 - Migrate to a hosted SQL platform so we have a place to persistently and continuously store our voting data since SQLite is not built for such an application use-case.
 - Add a commenting feature to the application so users can provide more specific feedback about the meal.
 - Add other menu items, including Halal section, etc.
    - Provide a settings page for users to indicate their dietary profile so we only display the appropriate dishes (only halal if you're halal, etc.)
