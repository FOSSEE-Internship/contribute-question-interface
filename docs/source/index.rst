.. Question Contribution documentation master file, created by

Welcome to Question Contribution's documentation!
=================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Basic Instructions
------------------

	1. Create 5 Python Coding Questions along with 5 test cases each on the above interface.
	2. Avoid trivial questions such as Printing patterns, Reversing strings, Arithmetic operations, etc.
	3. Question description should be grammatically correct and easy to understand.
	4. Questions can be original or adapted from other sources with significant changes in case the question is adapted, the source needs to be cited in the interface). We prefer non-cited, original questions for shortlisting the candidates.
	5. Question should be well tested.



Login & Register
----------------

	1. Click on the **Register** button on the main page.
	2. After registration login with the username and password


Creating Questions
------------------
	
	.. note::  You are allowed to create only 5 questions. You can edit and delete those questions though.

	1. After login click on **Start Contribution** button to start creating questions.
	2. On the contribution interface you can view all your questions.
	3. To delete a question Select the question and click on **Delete Question** button. Once deleted, a question cannot be  retrieved back. Please take caution before deletion.
	4. Click on **Add Question** button to create a new question.
	5. Below image shows an example of creating a question
			.. figure:: images/create_questions.jpg

		Fields to fill while creating questions
		
		* **Summary**- Short summary or the name of the question. Cannot be more than 256 characters.

		* **Points** - Points is the marks for a question. It can be in decimal digits.

		* **Description** - Write the actual question here. One can use HTML tags to format question text.

			.. note::  To add code snippets in question description please use html <pre>, <code> and <br> tags.

		* **Solution** - It is the **correct code answer** of the question. Please follow Python syntaxes here.
			For e.g. :: 

				a = input()
				b = input()
				print(a+b) 

		* **Citation** - Mention the reference url of the question if the question is adapated. Please make sure to cite the original source of the question if it is not a original question.

			.. note:: Leave the field blank if the question is original.

		* **Originality** - Specify whether the question is **Original Question** or **Adapted Question**

	6. Below image shows an example of how to create test cases.
			.. figure:: images/create_testcases.jpg

		In **Expected input** field, enter the value(s) that will be passed to the code through a standard I/O stream.

			.. note::  If there are multiple input values in a test case, enter the values in a new line as shown in figure.

		In **Expected Output** Field, enter the expected output for that test case. For e.g type 3 if the output of the user code is 3.

		To delete a test case Select **Delete** checkbox and click on **Check and Save** to delete the testcase and save the question.

			.. note::  Please do not change the type of the testcase i.e **stdiobasedtestcase**.

	7. If all the test cases for the questions pass, then the question is automatically approved. To see how many questions are approved, you can look at the **status** column in contribution page, where you see all your questions.

	8. If you have created 5 approved questions, **your question creation task is completed.**



