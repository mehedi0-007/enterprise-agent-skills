# Custom Button

Bad:
```html
<div class="button" onclick="save()">Save</div>
```

Problem:
- wrong semantics
- keyboard behavior must be recreated
- focus behavior must be recreated

Better:
```html
<button type="button">Save</button>
```
