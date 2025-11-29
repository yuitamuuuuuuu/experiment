class Experiment {
    constructor() {
        this.words_red = ["корона", "развитие", "душа", "время", "друг", "стекло", "лошадь"];
        this.words_blue = ["привычка", "камень", "лампа", "мелодия", "симпатия", "медицина", "офис"];
        this.words_gray = ["деревня", "газета", "деньги", "ручка", "птица", "смелость", "цирк"];
        
        this.conditions = [
            {color: "#E53935", label: "Red", words: [...this.words_red]},
            {color: "#1E88E5", label: "Blue", words: [...this.words_blue]},
            {color: "#BDBDBD", label: "Gray", words: [...this.words_gray]}
        ];
        
        this.currentCondition = 0;
        this.currentWord = 0;
        this.data = [];
        this.participantId = "";
        this.group = "";
        
        this.shuffleConditions();
    }

    shuffleConditions() {
        for (let i = this.conditions.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.conditions[i], this.conditions[j]] = [this.conditions[j], this.conditions[i]];
        }
    }

    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }

    startExperiment() {
        this.participantId = document.getElementById('participantId').value.trim();
        if (!this.participantId) {
            alert("Бля, введи ID сначала!");
            return;
        }

        this.group = Math.random() > 0.5 ? "A" : "B";
        
        const instructionText = this.group === "A" 
            ? "Вам будут показаны слова. Ваша задача — просто внимательно смотреть на них."
            : "Вам будут показаны слова. Ваша задача — запомнить слова, чтобы потом воспроизвести их в порядке показа.";
        
        document.getElementById('instructionText').textContent = instructionText;
        this.showScreen('instructionScreen');
    }

    startTrials() {
        this.currentCondition = 0;
        this.currentWord = 0;
        this.runCondition();
    }

    runCondition() {
        if (this.currentCondition >= this.conditions.length) {
            this.showScreen('endScreen');
            this.downloadData();
            return;
        }

        const condition = this.conditions[this.currentCondition];
        document.body.style.backgroundColor = condition.color;
        this.showScreen('wordScreen');
        
        this.showWordsSequentially(condition.words, 0);
    }

    showWordsSequentially(words, index) {
        if (index >= words.length) {
            setTimeout(() => {
                document.body.style.backgroundColor = "white";
                this.showInputScreen();
            }, 500);
            return;
        }

        document.getElementById('wordDisplay').textContent = words[index];
        document.getElementById('wordDisplay').style.color = "black";

        setTimeout(() => {
            this.showWordsSequentially(words, index + 1);
        }, 2000);
    }

    showInputScreen() {
        document.getElementById('userInput').value = '';
        this.showScreen('inputScreen');
        document.getElementById('userInput').focus();
        
        // Добавляем обработчик Enter
        document.getElementById('userInput').onkeydown = (e) => {
            if (e.key === 'Enter') {
                this.submitResponse();
            }
        };
    }

    submitResponse() {
        const response = document.getElementById('userInput').value.trim();
        const condition = this.conditions[this.currentCondition];
        
        this.data.push({
            participant: this.participantId,
            group: this.group,
            condition: condition.label,
            shown_words: condition.words.join(' '),
            typed_response: response,
            timestamp: new Date().toISOString()
        });

        this.currentCondition++;
        
        if (this.currentCondition < this.conditions.length) {
            this.showPauseScreen();
        } else {
            this.runCondition();
        }
    }

    showPauseScreen() {
        this.showScreen('pauseScreen');
        let seconds = 30;
        const countdownElement = document.getElementById('countdown');
        
        const interval = setInterval(() => {
            countdownElement.textContent = `Осталось: ${seconds} секунд`;
            seconds--;
            
            if (seconds < 0) {
                clearInterval(interval);
                this.runCondition();
            }
        }, 1000);
    }

    downloadData() {
        const csv = this.convertToCSV();
        const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv; charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `results_${this.participantId}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    convertToCSV() {
        const headers = ['participant', 'group', 'condition', 'shown_words', 'typed_response', 'timestamp'];
        let csv = headers.join(',') + '\n';
        
        this.data.forEach(row => {
            const rowData = headers.map(header => {
                let value = row[header] || '';
                // Экранируем кавычки и запятые
                if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                    value = '"' + value.replace(/"/g, '""') + '"';
                }
                return value;
            });
            csv += rowData.join(',') + '\n';
        });
        
        return csv;
    }
}

// Создаем глобальный объект эксперимента
const experiment = new Experiment();

// Глобальные функции для кнопок
function startExperiment() {
    experiment.startExperiment();
}

function startTrials() {
    experiment.startTrials();
}

function submitResponse() {
    experiment.submitResponse();
}
