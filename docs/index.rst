.. Question Contribution documentation master file, created by

Welcome to Question Contribution's documentation!
=================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Basic Instructions
------------------

    1. Create 5 Python Coding Questions with good quality test cases for each question.(expected 5 test cases).
    2. Avoid trivial questions such as Printing patterns, Reversing strings, Arithmetic operations, etc.
    3. Question description should be grammatically correct and easy to understand.
    4. Questions can be original or adapted from other sources with significant changes in case the question is adapted, the source needs to be cited in the interface. We prefer non-cited, original questions for shortlisting the candidates.
    5. All questions should be well tested.



Register & Login
----------------
    1. Click on the **Register** link on the |location_link|.

    .. |location_link| raw:: html

        <a href="https://contribute-yaksh.fossee.in/login/" target="_blank">main page</a>

    2. After registration, login with the username and password.


Creating Questions
------------------
    
    .. note::  You are allowed to create only 5 questions. You can edit and delete those questions though. Also please make sure questions are created using Python 3.x.

    1. After login click on **Start Contribution** button to start creating questions.
    2. On the contribution interface you can view all your questions.
    3. Click on **Add Question** button to create a new question.
        .. note:: Right click on the image and select **Open image in new tab** to view image properly.
    4. Below image shows an example of creating a question.
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
                print(int(a)+int(b))

        * **Citation** - Mention the reference url of the question if the question is adapted. Please make sure to cite the original source of the question if it is not a original question.

            .. note:: Leave the field blank if the question is original.

        * **Originality** - Specify whether the question is **Original Question** or **Adapted Question**

    5. Below image shows an example of how to create test cases.
            .. figure:: images/create_testcases.jpg

        In **Expected input** field, enter the value(s) that will be passed to the code through a standard I/O stream.

            .. note::  If there are multiple input values in a test case, enter the values in a new line as shown in figure.

        In **Expected Output** Field, enter the expected output for that test case. For e.g type 3 if the output of the user code is 3.

        To delete a test case, Select **Delete** checkbox and click on **Check and Save** to delete the testcase and save the question.

        To **add a new test case**, select ``stdio`` from the drop down box, found just above the ``Check and Save`` button.

    6. To delete a question, Select the question and click on **Delete Question** button. Once deleted, a question cannot be retrieved back. Please take caution before deletion.
    7. If all the test cases for the questions pass, then the question is automatically approved. To see how many questions are approved, you can look at the **status** column in contribution page, where you see all your questions.

    8. If you have created 5 approved questions, **your question creation task is completed.**

Reviewing Questions
-------------------
    1. After login, click on **Start Contribution** button to start reviewing questions.
    2. On the contribution interface you can view all the questions to review.
    3. Click on the **Question sumary** link to review a question.
    4. Read the **question description** and try to solve it by writing the solution code. Click on **Check Answer** button to check if your solution passes the question creator's testcases. You will see errors for the testcases that do not pass. Read the errors properly and try to fix your solution.
    5. You can **skip** the question if you find the following reasons for not being able to solve the question -
        a. If the question is incomprehensible 
        b. If the question is comprehensible but its solution is too difficult.
        c. If the question is comprehensible and its solution is fairly easy, but the testcases provided are wrong for the question.
    
    .. note:: If you find any other problem other than the three mentioned reasons, you can add it in the comments field. Otherwise it can be kept blank.

    6. If you are able to solve the question, you will be automatically redirected to the **review submission** page. Here you have to review the following attributes of the question -

        a. Check if the Question summary and description provided are grammatically correct and simple to understand.
        b. If the marks/points provided by the question creator is worth the question. A really simple question should not have more than single digit marks and really tough question should have atleast high two digit marks.
        c. Check Citation for the following cases - 
            1. If the question is stated to be original, please investigate if the question is truly original. Check on the internet to see if the question is directly copied or influenced by a similar question.
            2. If the question has been cited from a source, please investigate if the cited source is correct or not.
            3. If the question is not directly copied but is a generic question, like print Armstrong numbers, or factorial of a number or prime number or Fibonacci sequence, please treat the question as original question. But please make sure that you rate the question less.
        d. Please check **Check Citation** checkbox if the mentioned citation is correct. **Do not check the Check Citation checkbox if an original question is found out to be copied or if a cited source is wrong.** In such a case, please mention the actual source of question in the comments section.
        e. Rate the question, according to the overall quality, originality and toughness of the question.
        f. Comment, if you have some insights or problems with the question. Although Comments are optional, they will be appreciated.

    7. Once a review is submitted, you will be taken back to the dashboard. You can always edit your review or submit review for other questions.
