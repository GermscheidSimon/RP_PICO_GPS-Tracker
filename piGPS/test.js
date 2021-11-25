

function* infinite() {
    let index = 0;

    while (true) {
        yield index++;
    }
}
const generator = infinite()
while (true){
    console.log(generator.next().value)
}