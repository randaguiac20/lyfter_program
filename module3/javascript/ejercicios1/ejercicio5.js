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
    let total = 0;
    // start with the first grade
    let highest = student.grades[0];
    let lowest = student.grades[0];
    // Iterate over each grade to get the highest and lowest
    for (const g of student.grades) {
        total += g.grade;
        // Get the highest
        if (g.grade > highest.grade) {
            highest = g;
        }
        // Get the lowest
        if (g.grade < lowest.grade) {
            lowest = g;
        }
    }

    return {
        name: student.name,
        gradeAvg: total / student.grades.length,
        highesGrade: highest.name,
        lowestGrade: lowest.name
    };
};

const result = getStudent(student);
console.log("Student information:", result);

