
//Edit Post
let editButtons=document.querySelectorAll(".edit-btn")
editButtons.forEach(element=>{
     element.addEventListener("click",()=>{
        let post_id=element.dataset.id
        console.log(post_id)
        let post=document.querySelector(`#post-${post_id}`).innerHTML
        element.style.display="none";
        document.querySelector(`#post-${post_id}`).innerHTML=`<textarea name="edit-content" id="edit-post-${post_id}">${post}</textarea> <button class="submit-post edit-btn" id="edit-save-${post_id}">Save</button>`
        
        let button = document.querySelector(`#edit-save-${post_id}`)
        button.addEventListener("click",()=>{
            let content =document.querySelector(`#edit-post-${post_id}`).value
            console.log(content)
            fetch(`edit/${post_id}`,{
            method: "PUT",
            body:JSON.stringify({
                body:content,
            })
        });
        document.querySelector(`#post-${post_id}`).innerHTML=content
        element.style.display="block";
        })
        
     })
 })

//Toggle like

let likeBtn =document.querySelectorAll(".bi")
likeBtn.forEach(element =>{
    element.addEventListener("click",()=>{
        let post_id=element.dataset.id
        let user=element.dataset.user
        let liked=element.attributes.fill.value.trim()==='red' ? true : false;
        
        console.log(user)
        fetch(`toggle_like/${post_id}`,{
            method: "PUT",
            body:JSON.stringify({
                liked :!liked
            })
        });
        
        let like_count=Number(document.querySelector(`#like-count-${post_id}`).innerText);
        if (liked){
            like_count=like_count-1
            document.querySelector(`#like-count-${post_id}`).innerText=`${like_count}`
            element.setAttribute("fill","black")
        }
        else{
            like_count=like_count+1
            document.querySelector(`#like-count-${post_id}`).innerText=`${like_count}`
            element.setAttribute("fill","red")
        }
    })
})


//Following

let followBtn=document.querySelectorAll(".follow-btn")

followBtn.forEach(element =>{
    element.addEventListener("click",()=>{
        let user_id=element.dataset.user 
        let followed=element.innerText.trim() ==="Follow"? true : false;
        
        fetch(`toggle_following/${user_id}`,{
            method:"PUT",
            body:JSON.stringify({
               followed:!followed
            })
        })
        if(followed){
            element.innerHTML="Unfollow"
            console.log("bsbxhsbhxb")
        }else{
            element.innerHTML="Follow"
        }
    })
})