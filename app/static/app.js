
const API_URL = "/api/contacts";

const form = document.querySelector("#contact-form");
const nameInput = document.querySelector("#name");
const mobileInput = document.querySelector("#mobile");
const emailInput = document.querySelector("#email");

const list = document.querySelector("#contacts-list");
const message = document.querySelector("#message");
const emptyMessage = document.querySelector("#empty-message");

const formTitle = document.querySelector("#form-title");
const submitButton = document.querySelector("#submit-button");
const cancelButton = document.querySelector("#cancel-button");
const refreshButton = document.querySelector("#refresh-button");

let editingId = null;


// Выполняет запрос и обрабатывает ошибки API
async function apiRequest(url, options = {}) {
    const response = await fetch(url, options);

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const detail = data?.detail;

        const errorText = Array.isArray(detail)
            ? detail.map(item => item.msg).join(", ")
            : detail;

        throw new Error(
            errorText || `Ошибка запроса: ${response.status}`
        );
    }

    return data;
}


// Показывает сообщение об ошибке
function showError(error) {
    message.textContent = error.message;
}


// Загружает список контактов
async function loadContacts() {
    list.replaceChildren();
    message.textContent = "";

    try {
        const contacts = await apiRequest(API_URL);

        emptyMessage.hidden = contacts.length !== 0;

        for (const contact of contacts) {
            list.appendChild(createContactCard(contact));
        }
    } catch (error) {
        emptyMessage.hidden = true;
        showError(error);
    }
}


// Создаёт карточку одного контакта
function createContactCard(contact) {
    const card = document.createElement("article");
    card.className = "contact-card";

    const title = document.createElement("h3");
    title.textContent = contact.name;

    const phone = document.createElement("p");
    phone.textContent = `Телефон: ${contact.mobile}`;

    const email = document.createElement("p");
    email.textContent = `Email: ${contact.email}`;

    const actions = document.createElement("div");
    actions.className = "card-actions";

    const editButton = document.createElement("button");
    editButton.textContent = "Изменить";
    editButton.className = "secondary";
    editButton.addEventListener("click", () => startEditing(contact));

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Удалить";
    deleteButton.className = "danger";
    deleteButton.addEventListener("click", () => deleteContact(contact.id));

    actions.append(editButton, deleteButton);
    card.append(title, phone, email, actions);

    return card;
}


// Переводит форму в режим редактирования
function startEditing(contact) {
    editingId = contact.id;

    nameInput.value = contact.name;
    mobileInput.value = contact.mobile;
    emailInput.value = contact.email;

    formTitle.textContent = "Изменить контакт";
    submitButton.textContent = "Сохранить";
    cancelButton.hidden = false;

    message.textContent = "";
    form.scrollIntoView({ behavior: "smooth", block: "start" });
}


// Возвращает форму в режим добавления
function resetForm() {
    editingId = null;
    form.reset();

    formTitle.textContent = "Добавить контакт";
    submitButton.textContent = "Добавить";
    cancelButton.hidden = true;
}


// Добавление или изменение контакта
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    message.textContent = "";

    const contactData = {
        name: nameInput.value.trim(),
        mobile: mobileInput.value.trim(),
        email: emailInput.value.trim(),
    };

    const isEditing = editingId !== null;

    const url = isEditing
        ? `${API_URL}/${editingId}`
        : API_URL;

    const method = isEditing ? "PUT" : "POST";

    try {
        await apiRequest(url, {
            method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contactData),
        });

        resetForm();
        await loadContacts();
    } catch (error) {
        showError(error);
    }
});


// Удаление контакта
async function deleteContact(id) {
    if (!confirm("Удалить этот контакт?")) {
        return;
    }

    message.textContent = "";

    try {
        await apiRequest(`${API_URL}/${id}`, {
            method: "DELETE",
        });

        if (editingId === id) {
            resetForm();
        }

        await loadContacts();
    } catch (error) {
        showError(error);
    }
}


// Обработчики кнопок
cancelButton.addEventListener("click", resetForm);
refreshButton.addEventListener("click", loadContacts);

// Загружаем контакты при открытии страницы
loadContacts();
