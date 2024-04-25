
// Later, prevent tab from switching (Vue event modifiers)


async function runCode(){
    let input = document.getElementById("py").value;
    console.log(input);                                         // TEMPORARY
    let response = await fetch("/run",{
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "py="+input
    });
    if (response.status == 200){
        let result = await response.text()
        console.log(result);                                    //TEMPORARY
        document.getElementById("answer").innerHTML = result;
    }
};