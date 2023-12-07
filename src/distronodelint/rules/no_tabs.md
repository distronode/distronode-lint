# no-tabs

This rule checks for the tab character. The `\t` tab character can result in
unexpected display or formatting issues. You should always use spaces instead of
tabs.

!!! note

    This rule does not trigger alerts for tab characters in the ``distronode.builtin.lineinfile`` module.

## Problematic Code

```yaml
---
- name: Example playbook
  hosts: all
  tasks:
    - name: Do not trigger the rule
      distronode.builtin.lineinfile:
        path: some.txt
        regexp: '^\t$'
        line: 'string with \t inside'
    - name: Trigger the rule with a debug message
      distronode.builtin.debug:
        msg: "Using the \t character can cause formatting issues." # <- Includes the tab character.
```

## Correct Code

```yaml
---
- name: Example playbook
  hosts: all
  tasks:
    - name: Do not trigger the no-tabs rule
      distronode.builtin.debug:
        msg: "Using space characters avoids formatting issues."
```
