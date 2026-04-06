async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');

    const content = document.createElement('span');
    content.textContent = `${n.title}: ${n.content}`;
    li.appendChild(content);

    const editBtn = document.createElement('button');
    editBtn.textContent = 'Edit';
    editBtn.style.marginLeft = '10px';
    editBtn.onclick = async () => {
      await editNote(n.id);
    };
    li.appendChild(editBtn);

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.style.marginLeft = '10px';
    deleteBtn.onclick = async () => {
      await deleteNote(n.id);
    };
    li.appendChild(deleteBtn);

    const extractBtn = document.createElement('button');
    extractBtn.textContent = 'Extract Action Items';
    extractBtn.style.marginLeft = '10px';
    extractBtn.onclick = async () => {
      await extractActionItems(n.id);
    };
    li.appendChild(extractBtn);

    list.appendChild(li);
  }
}

async function searchNotes(query) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const notes = await fetchJSON(`/notes/search/?q=${encodeURIComponent(query)}`);
  for (const n of notes) {
    const li = document.createElement('li');
    li.textContent = `${n.title}: ${n.content}`;
    list.appendChild(li);
  }
}

async function extractActionItems(noteId) {
  const resultsDiv = document.getElementById('extraction-results');
  const contentDiv = document.getElementById('extraction-content');

  try {
    const data = await fetchJSON(`/notes/${noteId}/extract`, { method: 'POST' });

    contentDiv.innerHTML = '';

    if (data.extracted_items.length === 0) {
      contentDiv.innerHTML = '<p>No action items found in this note.</p>';
    } else {
      contentDiv.innerHTML = '<p>Found ' + data.extracted_items.length + ' action item(s):</p>';

      const itemsList = document.createElement('ul');
      for (const item of data.extracted_items) {
        const itemLi = document.createElement('li');

        const itemDiv = document.createElement('div');
        itemDiv.style.marginBottom = '10px';

        const descSpan = document.createElement('span');
        descSpan.textContent = item.description;
        descSpan.style.fontWeight = 'bold';
        itemDiv.appendChild(descSpan);

        if (item.tags && item.tags.length > 0) {
          const tagsSpan = document.createElement('span');
          tagsSpan.textContent = ' Tags: ' + item.tags.join(', ');
          tagsSpan.style.color = '#666';
          tagsSpan.style.marginLeft = '10px';
          itemDiv.appendChild(tagsSpan);
        }

        const createBtn = document.createElement('button');
        createBtn.textContent = 'Create Action Item';
        createBtn.style.marginLeft = '10px';
        createBtn.onclick = async () => {
          await createActionItem(item.description);
          itemDiv.appendChild(document.createElement('span')).textContent = ' ✓ Created';
          createBtn.disabled = true;
          createBtn.style.opacity = '0.5';
        };
        itemDiv.appendChild(createBtn);

        itemLi.appendChild(itemDiv);
        itemsList.appendChild(itemLi);
      }

      contentDiv.appendChild(itemsList);
    }

    resultsDiv.style.display = 'block';
  } catch (error) {
    console.error('Failed to extract action items:', error);
    contentDiv.innerHTML = '<p style="color: red;">Failed to extract action items: ' + error.message + '</p>';
    resultsDiv.style.display = 'block';
  }
}

async function createActionItem(description) {
  await fetchJSON('/action-items/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description }),
  });
  loadActions();
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const items = await fetchJSON('/action-items/');
  for (const a of items) {
    const li = document.createElement('li');
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

async function editNote(noteId) {
  const title = prompt("Enter new title:");
  const content = prompt("Enter new content:");
  if (title && content) {
    await fetchJSON(`/notes/${noteId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    loadNotes();
  }
}

async function deleteNote(noteId) {
  if (confirm("Are you sure you want to delete this note?")) {
    await fetchJSON(`/notes/${noteId}`, { method: 'DELETE' });
    loadNotes();
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('search-button').addEventListener('click', async () => {
    const query = document.getElementById('search-input').value;
    if (query.trim()) {
      await searchNotes(query);
    }
  });

  document.getElementById('search-input').addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
      const query = e.target.value;
      if (query.trim()) {
        await searchNotes(query);
      }
    }
  });

  document.getElementById('clear-search').addEventListener('click', () => {
    document.getElementById('search-input').value = '';
    loadNotes();
  });

  document.getElementById('close-extraction').addEventListener('click', () => {
    document.getElementById('extraction-results').style.display = 'none';
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  loadNotes();
  loadActions();
});
