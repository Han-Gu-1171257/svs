# Selwyn Veterinary Services (SVS) Web Application  
# Han Gu | 1171257


---

## 💬 Discussion — My Design Decisions  

When I started improving my milestone version, I had this “brilliant” idea to make everything fit on one big dashboard — customers, appointments, services, everything together.  
In my head it sounded efficient, but in Flask it turned into chaos.  
Different queries mixed up, templates became impossible to read, and I couldn’t even tell which table a variable came from.  
After a few hours of frustration, I decided to give up and split them into separate routes and templates.  
That single change instantly made things easier to test, and it actually felt like a real application instead of a spaghetti mess.  

At first, all my SQL was written directly inside `app.py`.  
It worked fine for a while, but as the project grew, scrolling through hundreds of lines became painful.  
One night I forgot to close a connection and the whole thing froze on PythonAnywhere.  
That’s when I decided to make a separate file called `db.py`.  
It just has simple functions like `init_db()` and `fetch_all()`, but it changed everything — now I can fix or test database logic without touching the main routes.  
Later, when I had to update the connection settings for PythonAnywhere, I only had to change one line.  
That’s when I realised what “modular code” really means in practice.  

After a week, I also went back and rewrote all my queries to use `%s` placeholders.  
Before that, I was lazily using string concatenation because it “just worked”.  
It did — until it didn’t.  
One of my test queries completely broke on the server, and that was the wake-up call I needed.  
Now every query runs safely through `execute()` and I feel way more confident about my database.  

Validation was another small but important lesson.  
I had disabled Sundays in the HTML date picker, but then I realised someone could still submit a Sunday booking using curl.  
At first I was surprised, then I remembered what Richard said: “never trust the front end.”  
So I added another check in Flask that rejects Sunday bookings before they even reach the database.  
Now the system shows an alert in the browser and flashes an error message on the backend.  
It’s simple, but it made me appreciate how “defensive coding” actually works.  

For a bit of personality, I added my own custom 404 and 500 pages.  
It’s nothing major, but it makes the app feel friendlier and less like a student project.  

Later, after coding late into the night, I noticed my eyes were tired from the bright white background.  
So I added an automatic dark mode using the browser’s `prefers-color-scheme` setting.  
It wasn’t part of the requirements, but it made a big difference for me personally.  
I didn’t measure contrast ratios or anything scientific — just kept tweaking colours until the text looked readable in both modes.  
It’s funny how something that started as a “comfort fix” ended up teaching me about accessibility.  

The biggest challenge for me was connecting to MySQL on PythonAnywhere.  
Everything worked perfectly on my laptop, but once uploaded, the database refused to connect.  
I spent two nights reading logs before realising it used a slightly different driver.  
I finally fixed it by rewriting my `init_db()` with a `try/except` block and printing a clearer error message.  
When it finally worked at 2 a.m., I actually said “thank you” out loud to my computer.  
That moment really showed me that debugging deployment issues takes a totally different kind of patience.  

Another small victory came when I noticed I had written the same long JOIN three times.  
I got annoyed enough to stop what I was doing and refactor.  
Now I just use `fetch_all()` everywhere, and if I ever need to add logging or extra debugging later, I can do it in one place.  
It’s such a small change, but it makes the code feel much cleaner.  

I almost added a delete button for customers and appointments, but then I realised it might break the service summary report.  
Deleting one row could cause all kinds of issues with totals and foreign keys.  
To be honest, I didn’t have time to fix that properly, so I just left it out.  
It’s one of those cases where keeping the app stable was more important than adding another feature.  

Compared to my milestone version, this one feels more structured, safer, and easier to understand.  
Every part has a clear job, the code reads cleaner, and the bugs are easier to find.  
It’s still not perfect, but it finally feels like something I could actually maintain — not just a demo that barely holds together.  

---

## 🗃️ Database Questions  

### 1 What is the database model used in your web app?  

It follows a relational model with four tables:  

```
customers (customer_id, first_name, family_name, email, phone, date_joined)
services (service_id, service_name, price)
appointments (appt_id, customer_id, appt_datetime, notes)
appointment_services (appt_id, service_id)
```

Each customer can have many appointments, and each appointment can include multiple services.  
This matches the SQL scripts provided in the brief.  

---

### 2 How are SQL queries protected against injection?  

All SQL queries use parameter placeholders (`%s`):  

```python
cur.execute("SELECT * FROM customers WHERE family_name LIKE %s;", (q,))
```

No query strings are concatenated manually.  
I tested this on PythonAnywhere and confirmed all user inputs were safely handled.  

---

### 3 Future Improvement — Animals Table  

If I had more time, I’d like to add an `animals` table that links each pet to its owner.  
Here’s an example SQL statement to create it:  

```sql
CREATE TABLE animals (
  animal_id INT AUTO_INCREMENT PRIMARY KEY,
  owner_id INT NOT NULL,
  name VARCHAR(80),
  species VARCHAR(50),
  sex ENUM('M','F'),
  date_of_birth DATE,
  FOREIGN KEY (owner_id) REFERENCES customers(customer_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);
```

And an example insert:  

```sql
INSERT INTO animals (owner_id, name, species, sex, date_of_birth)
VALUES (103, 'Milo', 'Cat', 'M', '2022-06-18');
```

It wasn’t part of this version, but it would make the system more realistic for clinics that track pets individually.  
For now, I just documented the idea.  

---


### References
Stockcake. (n.d.). [Dog veterinary visit]. https://stockcake.com/i/dog-veterinary-visit_978219_849609

