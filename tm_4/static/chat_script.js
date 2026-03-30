

async function loadCat(){
    let link = "https://cataas.com/cat"
    try{
        let reponse = await fetch(link);
        if (!reponse.ok)
        {
            throw new Error('reponse status:  ${reponse.status}');
        }
        let result = await reponse.json();
        const img = URL.createObjectURL(result)
        document.getElementById("img_chat").img.src=img
        //console.log(result);
    }
    catch(error){
        console.error(error.message)
    }
     
}