// /* All of my JS code will go here */

/* I will use vanilla JS, edit the post using the innerHTML property, and send the edition to the database using
JSON. I’d rather forget about React for the time being for this question.

So, to edit a specific post using JS, I will add an “onclick()” or “onsubmit” on each post using Jinja notation,
and the argument of that event listener will be that post’s ID, which I can call by using “post.ID”. So, I may add
something like “onclick(‘{{post.id}}’)” to the “Edit” link.

I will modify the “Edit” link so that it becomes a button, so that it’s easier to handle with JS code.

Now, whenever the user clicks on the “Edit button”, I will render a <textarea> tag. I can do that by using editing the 
innerHTML attribute of the div that contains the ID of that specific post. I can get that <div> by using a 
getElementByID selector.

Now, I need to prepopulate the <textarea> that appears with the body of that post. I need to use an API and the fetch() 
function for this. Or, to make things simpler, I could simply store the HTML of that div into a variable, and then 
I could insert that variable into the <textarea> being rendered by the double ticks and the innerHTML attribute. To 
sget the content of the post’s body, I can simply call innerHTML.

I’m on the right track. However, I’m also getting the <p> tags of the body of that post, which I don’t want. I only want 
the text inside those <p> tags. To get them, I will use textContent attribute from JS (source: 
https://bobbyhadz.com/blog/javascript-get-text-of-paragraph .) I will use “variable_with_text.textContent” to get only 
the text from the post’s body without getting the <p> tags.

It’s working. Now, I’m getting extra space both before and after the text of the post. To remove it, I’ll try to use 
the trim() function from JS (source: https://bobbyhadz.com/blog/javascript-get-text-of-paragraph .)

I will add code so that the “edit” button makes the “Save” button appear.

After further consideration, I realize that the fetch() function (if I manually specify it) will always send a POST 
request, independently of whether I use a form or a button for the “Save” button. So, for the sake of simplicity, I 
will use a <button> tag for the “Save” button.

I will add a “onclick()” even listener to the “Save” button, which will obtain the ID of that post to differentiate 
that post from other posts. Also, I will call the function that will fetch the API from the edit_post() view. But, 
for that, I need to create that “save()” function beforehand.

The full explanation of the save() function is given on the views.py file. But, in a nutshell, the save() function
will call the edit_page() API via a fetch() call to store the edited post in the database. I also need the text
of the edited post in the save() function. So, to get that, I will assign an ID number to the <textarea> generated
by the edit() function. Then, I will get that <textarea> with that ID number with a document.getElementById() in
the save() function and get the text from it.

*/

/* This creates a cookie (source: anonymous's reply on
https://stackoverflow.com/questions/43606056/proper-django-csrf-validation-using-fetch-post-request ). 

This is needed to be able to have the CSRF protection activated without getting any bugs from fetch() calls. 

*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




/* This detects if the <textarea> text has been modified. 
The solution will be to use the “oninput” JS event listener, which executes code each time a user types a letter on a 
<textarea> field (source: https://www.w3schools.com/jsref/event_oninput.asp .) To use this, I will have to create a 
3rd JS function, which will get the edited text from the <textarea> I could call it something like “edited_text(argument)”. 
That function will be called on either the save() function, or it will be an independent function. Then, I 
will call it from the save() function to get the edited text from the post. I will add the event listener to 
the <textarea> code, which is generated on the edit() function. Finally, the save() function will send that 
edited text from the JS code to the view. 

I need the post's ID on the "oninput" function (edited_text()) as an argument, since I need to differentiate that post 
from the other posts.

What I can do is that, each time that the “oninput” even listener is called, that is, each time that the edit_text() function 
is called, I will edit the HTML code of the <textarea> by using the innerHTML attribute. That way, the text will be constantly 
be edited on the HTML. Then, when I click on “Save”, the edited text will be sent to the API. I could use code like this 
(source: https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_oninput ):
    let text = document.getElementById("id_of_textarea").value;
    document.getElementById("id_of_textarea").innerHTML = text;

    It should work with just using “=” in the snippet that ends with “innerHTML”. That is, it should work without using “+=”. In 
other words, if I delete something from the existing text, and if I don’t add any additional text, it should still get all of 
the text properly.

BUG FIX: The above didn’t work properly, but that was because I'm also grabbing the "value" attribute. That is, I was doing 
"code.value.innHTML", which could have caused a bug. So, I will make a new variable that will get the text 
from the <textarea>, and replace it with what the user has typed so far by using a getElementByID, and then using
"innerHTML".

*/
function edited_text(post_id) {
    
    // DEBUG msg: This will execute each time that the user types anything in the <textarea>
    console.log(`You typed/deleted something from a <textarea> in the post with ID number ${post_id}.`);

    // This edits the text of the <textarea> in the HTML code whenever the user types something
    let text = document.getElementById(`textarea_${post_id}`).value;
    // text.innerHTML = text;

    // DEBUG msg: This is what the user has typed
    console.log(`You have written "${text}"`);

    // This replaces the HTML code from the <textarea> to include what the user has typed
    document.getElementById(`textarea_${post_id}`).innerHTML = text;

}

// Edit post mechanic
function edit(post_id) {

    // DEBUG msg
    console.log(`This is post number ${post_id}`)

    // This gets the div with the post's body
    let post = document.getElementById(`${post_id}`)

    // This stores the text of the post's body
    let post_body = post.textContent.trim()

    // This renders the <textarea> tag that replaces the post's body
    post.innerHTML = `
    <textarea id="textarea_${post_id}" 
    oninput="edited_text(${post_id})">${post_body}</textarea>
    `

    // This stores the save button
    let save_button = document.getElementById(`save_button_${post_id}`)

    // This renders the "Save" button
    save_button.innerHTML = `
    <button class="btn btn-primary" onclick="save(${post_id})">Save</button>
    `

}

/* Function for saving edited posts 

After saving the post, I will remove the <textarea>, and I will put the post's text between <p> tags, so that the post
looks normal after clicking on the "Save" button. To do that, I need to edit the <div> that contains the <textarea>, 
NOT the <textarea> itself.

Now, I want to make the “Save” button to disappear after clicking on it.

This is what I’ll do: I will use a huge code snippet to reate a cookie, and then insert it into the fetch() call to update 
the post with the CSRF protection on (source: anonymous's reply on 
https://stackoverflow.com/questions/43606056/proper-django-csrf-validation-using-fetch-post-request .) First, I will use 
the getCookie() function made by anonymous in the previously mentioned link. Then, on the “save()” function, I will edit the 
fetch() call to eliminate the “headers” attribute, and then specify the POST request and include the “credentials: same origin” 
attribute into the fetch() call. I also need to create a variable that gets the cookie for the CSRF call.

*/
function save(post_id) {

    // DEBUG msg
    console.log(`You have clicked "Save" on post number ${post_id}`)

    // This creates a cookie for the CSRF token
    let csrftoken = getCookie('csrftoken');

    // This gets the <textarea> with the edited text from the post
    let post = document.getElementById(`textarea_${post_id}`)

    // This stores the text of the post's body without spaces nor tags
    let post_body = post.textContent.trim()


    /* This will call the API to update the post in the database. I added an extra header to add
    a cookie to the fetch() call so that it doesn't give me problems while using CSRF protection.*/
    fetch(`/edit/${post_id}`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Accept': 'application/json, text/plain, */*',
            'Content-type':'application/json'
        },
        body:JSON.stringify({body:post_body, post_id:post_id})                
    })

    // This gets the div with the post's body
    let post_div = document.getElementById(`${post_id}`)

    // This transforms the <textarea> tags into <p> tags
    post_div.innerHTML = `
    <p>${post_body}</p>
    `

    // This stores the save button's div
    let save_button = document.getElementById(`save_button_${post_id}`)

    // This eliminates the "Save" button
    save_button.innerHTML = ''
}




















// /* It would be best to type the HTML code for the buttons using React in the JS file, NOT directly in the HTML file. */

// /* I will make the button using React. So, I will create a <div> that will render the Follow/Unfollow
// button, and I will assign it an ID. Then, I will go to the JS file, and I will create a function that
// will render the button. I need to use “ReactDOM.render”, and use a querySelector (or a getElementByID)
// to get the div that will store the button, and render it. And, of course, I need to create the function
// that will render “Follow” or “Unfollow” when a user clicks on the button. Source of all of this: Brian’s
// “User Interfaces” lecture: https://youtu.be/jrBhi8wbzPw

// The 1st parameter of the "const" variable checks if the button says "Follow" or "Unfollow". Meanwhile,
// the 2nd parameter will modify the state from "Follow" to "Unfollow", or vice-versa. The default state
// will be "Follow". However, I ideally I should check the database to see whether I should render
// "Follow" or "Unfollow". I cannot assume that the user is not following another user if they
// enter into someone else's profile page.

// To check if the user is following or not another user, I will use an "if" statement, and
// I will use an API and a fetch() function to check if the user is following the other user.

// In the "const" variable (which I could name "let" or "var", since its original value may change
// depending on whether the user is already following someone), I could make a fetch call()
// to check whether the user has any followers on the Follow table. If they don't have any followers,
// the initial state of the button should be follow. So, once I create the API to fetch the
// Follow table, I will add an "if" statement, and I will specify whether "React.useState()"
// should initially be "Follow" or "Unfollow".

// I will put the button outside of the React div. The React div will be empty, and won’t render anything until
// the user clicks on the “follow” button. Then, if the user clicks on the button, one of 2 things will happen
// with an “if” statement: 1) I will get the original button, delete it, and rebuild it, but this time, it will
// display the word “unfollow”. 2) The same as the previous condition, but I will render the word “follow”.

// */
// function Follow_or_unfollow_user() {

//     // This will get the current word that's being displayed on the "follow/unfollow" button
// //    currentButtonState = document.querySelector("#follow_or_unfollow")

//     // This breaks my code
// //    currentButtonState = document.getElementByID("follow_or_unfollow")

//     // This stores whether the button should say "follow" or "unfollow"
//     const [isFollowing, setFollowState] = React.useState("Follow");

//     // This will toggle the button to "follow" or "unfollow" if the user clicks on it
//     function updateFollowState() {

//         // If the button says "follow", I will change it to "unfollow"
//         if (isFollowing == "Follow") {
//             setFollowState("Unfollow");
//         }
//         else {
//             setFollowState("Follow");
//         }

//     }

//     // This is the HTML code for the button
//     return (
//         <button id="follow_or_unfollow" class="btn btn-primary" onClick={updateFollowState}>
//             {isFollowing}
//         </button>
//     );
// }

// // This renders the button
// ReactDOM.render(<Follow_or_unfollow_user />, document.querySelector("#follow_unfollow_container"));


// /* This will render the "Follow" button */
// //function Follow_button() {
// //    return (
// //        <div>Follow Button</div>
// //    );
// //}
// //
// //ReactDOM.render(<Follow_button />, document.querySelector("#follow_button"));


// /* This will render the "Unfollow" button */
// //function Unfollow_button() {
// //    return (
// //        <div>Unfollow Button</div>
// //    );
// //}
// //
// //ReactDOM.render(<Unfollow_button />, document.querySelector("#unfollow_button"));


// /* I will make the button using React. So, I will create a <div> that will render the Follow/Unfollow 
// button, and I will assign it an ID. Then, I will go to the JS file, and I will create a function that 
// will render the button. I need to use “ReactDOM.render”, and use a querySelector (or a getElementByID) 
// to get the div that will store the button, and render it. And, of course, I need to create the function 
// that will render “Follow” or “Unfollow” when a user clicks on the button. Source of all of this: Brian’s 
// “User Interfaces” lecture: https://youtu.be/jrBhi8wbzPw 

// The 1st parameter of the "const" variable checks if the button says "Follow" or "Unfollow". Meanwhile,
// the 2nd parameter will modify the state from "Follow" to "Unfollow", or vice-versa. The default state
// will be "Follow". However, I ideally I should check the database to see whether I should render 
// "Follow" or "Unfollow". I cannot assume that the user is not following another user if they
// enter into someone else's profile page.

// To check if the user is following or not another user, I will use an "if" statement, and 
// I will use an API and a fetch() function to check if the user is following the other user.

// In the "const" variable (which I could name "let" or "var", since its original value may change
// depending on whether the user is already following someone), I could make a fetch call()
// to check whether the user has any followers on the Follow table. If they don't have any followers,
// the initial state of the button should be follow. So, once I create the API to fetch the 
// Follow table, I will add an "if" statement, and I will specify whether "React.useState()"
// should initially be "Follow" or "Unfollow".

// */
// //function Follow_or_unfollow_user() {
// //
// //    // This stores whether the button should say "follow" or "unfollow"
// //    const [isFollowing, setFollowState] = React.useState("Follow");
// //
// //    // This will toggle the button to "follow" or "unfollow" if the user clicks on it
// //    function updateFollowState() {
// //
// //        // If the button says "follow", I will change it to "unfollow"
// //        if (isFollowing == "Follow") {
// //            setFollowState("Unfollow");
// //        }
// //        else {
// //            setFollowState("Follow");
// //        }
// //
// //    }
// //
// //    // This is the HTML code for the button
// //    return (
// //        <button className="btn btn-primary" onClick={updateFollowState}>{isFollowing}</button>
// //    );
// //}
// //
// //// This renders the button
// //ReactDOM.render(<Follow_or_unfollow_user />, document.querySelector("#follow_or_unfollow"));
// //


// /* This will let me test if my React code works (source:
// https://youtu.be/jrBhi8wbzPw ).

// This gives me an error in the console if I enter into a profile page */
// function Test() {
//     return (
//         <div>Hello, world!</div>
//     );
// }

// ReactDOM.render(<Test />, document.querySelector("#react-test"));

// console.log("This is written via the JS file, but without using React.")

// /* This will test if the "follow" button works when clicked */
// function Follow_button_test() {
//     console.log("You just clicked on the Follow/Unfollow button.")

//     // This will empty the div if the user clicks on the unfollow button
//     document.querySelector("#follow_or_unfollow_div").innerHTML = ''


// }
// //    return (
// //        <div><b>You clicked on the Follow/Unfollow button</b></div>
// //    );
// //}
// //
// //ReactDOM.render(<Follow_button_test />, document.querySelector("#follow_or_unfollow_div"));
