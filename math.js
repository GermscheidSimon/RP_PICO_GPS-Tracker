let num = 0

function compound(principal, length, interest, saved, index) {
    let newprincipal = (principal * interest) + saved
    if (index <= length) {
        index++
        num = newprincipal
        compound(newprincipal, length, interest, saved, index)
    } 
}
const age34 = compound(13900, 10, 1.15, 15000, 1)
console.log('age34', num)
const age44 = compound(num, 10, 1.10, 20000, 1)
console.log('age44', num)