/* 
Realiza un programa que reciba el siguiente objeto, 
e imprima otro objeto con los siguientes datos

// Entrada
const student = {
	name: "John Doe",
	grades: [
		{name: "math",grade: 80},
		{name: "science",grade: 100},
		{name: "history",grade: 60},
		{name: "PE",grade: 90},
		{name: "music",grade: 98}
	]
}

const result = {
	name: "John Doe",
	gradeAvg: 85.6,
	highesGrade: "science",
	lowestGrade: "history"
}

*/


const student = {
    name: "John Doe",
    grades: [
        { name: "math", grade: 80 },
        { name: "science", grade: 100 },
        { name: "history", grade: 60 },
        { name: "PE", grade: 90 },
        { name: "music", grade: 98 }
    ]
};

const getStudent = (student) => {
    // Sum all grades and divide by count
    const total = student.grades.reduce((sum, g) => sum + g.grade, 0);
    const gradeAvg = total / student.grades.length;

    // Find the object with the highest grade
    // ? = if
    // : = else
    const highest = student.grades.reduce((max, g) => g.grade > max.grade ? g : max);

    // Find the object with the lowest grade
    const lowest = student.grades.reduce((min, g) => g.grade < min.grade ? g : min);

    return {
        name: student.name,
        gradeAvg: gradeAvg,
        highesGrade: highest.name,
        lowestGrade: lowest.name
    };
};

const result = getStudent(student);
console.log("Student information:", result);

