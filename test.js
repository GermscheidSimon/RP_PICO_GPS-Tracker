

// function* infinite() {
//     let index = 0;

//     while (true) {
//         yield index++;
//     }
// }
// const generator = infinite()
// while (true){
//     console.log(generator.next().value)
// }


function trisum(n, csum){
    if(n == 0){
        return csum
    }
    else{
        console.log(csum)
        return trisum(n - 1, csum + n)
    }
}

console.log(trisum(2, 0))
