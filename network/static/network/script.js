/* All of my JS code will go here */

/* I will make the button using React. So, I will create a <div> that will render the Follow/Unfollow 
button, and I will assign it an ID. Then, I will go to the JS file, and I will create a function that 
will render the button. I need to use “ReactDOM.render”, and use a querySelector (or a getElementByID) 
to get the div that will store the button, and render it. And, of course, I need to create the function 
that will render “Follow” or “Unfollow” when a user clicks on the button. Source of all of this: Brian’s 
“User Interfaces” lecture: https://youtu.be/jrBhi8wbzPw 

The 1st parameter of the "const" variable checks if the button says "Follow" or "Unfollow". Meanwhile,
the 2nd parameter will modify the state from "Follow" to "Unfollow", or vice-versa. The default state
will be "Follow". However, I ideally I should check the database to see whether I should render 
"Follow" or "Unfollow". I cannot assume that the user is not following another user if they
enter into someone else's profile page.

To check if the user is following or not another user, I will use an "if" statement, and 
I will use an API and a fetch() function to check if the user is following the other user.

In the "const" variable (which I could name "let" or "var", since its original value may change
depending on whether the user is already following someone), I could make a fetch call()
to check whether the user has any followers on the Follow table. If they don't have any followers,
the initial state of the button should be follow. So, once I create the API to fetch the 
Follow table, I will add an "if" statement, and I will specify whether "React.useState()"
should initially be "Follow" or "Unfollow".

*/
//function Follow_or_unfollow() {
//
//    // This stores whether the button should say "follow" or "unfollow"
//    const [isFollowing, setFollowState] = React.useState("Follow");
//
//    // This will toggle the button to "follow" or "unfollow" if the user clicks on it
//    function updateFollowState() {
//
//        // If the button says "follow", I will change it to "unfollow"
//        if (isFollowing == "Follow") {
//            setFollowState("Unfollow");
//        }
//        else {
//            setFollowState("Follow");
//        }
//
//    }
//
//    // This is the HTML code for the button
//    return (
//        <button className="btn btn-primary" onClick={updateFollowState}>{isFollowing}</button>
//    );
//}
//
//// This renders the button
//ReactDOM.render(<Follow_or_unfollow />, document.querySelector("#follow_or_unfollow"));
//


/* This will let me test if my React code works (source: 
https://youtu.be/jrBhi8wbzPw )  */
function Test() {
    return (
        <div>Hello, world!</div>
    );
}

ReactDOM.render(<Test />, document.querySelector("#react-test"));

console.log("This is written via the JS file, but without using React.")