def admonition(extra_classes, children=None):
    children_str = ''
    if children:
        children_str = '\n'.join(children)
    return f'<div class="admonition {extra_classes}">{children_str}</div>'


def admonition_title(title):
    return f'<p class="admonition-title">{title}</p>'


def text_question(title, question, answer_text, extra_classes=''):
    return admonition(f'question {extra_classes}', [
        admonition_title(title),
        p(question),
        answer('Answer', answer_text)
    ])


def answer(title, text):
    return admonition('answer', [
        admonition_title(title),
        p(text)
    ])


def el(tag, children=None):
    children_str = ''
    if children:
        children_str = '\n'.join(children)
    return f'<{tag}>{children_str}</{tag}>'


def div(children=None):
    return el('div', children)


def p(text):
    return el('p', [text])


def form(children=None):
    return el('form', children)


def task_list(choices, answer_text):
    return f'''
    <ul class="task-list">
      {''.join(choice(c) for c in choices)}
    </ul>
    {answer('Answer', answer_text)}
    '''


def choice(label):
    return f'''
    <li class="task-list-item">
      <label class="task-list-control">
        <input type="checkbox">
        <span class="task-list-indicator"></span>
      </label> {label}
    </li>
    '''
