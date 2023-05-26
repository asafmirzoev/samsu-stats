$(document).on('change', '#faculty', function() {

    let faculty = $(this).find(":selected").val();
    let course_select = $('#course');
    let direction_select = $('#direction');
    let group_select = $('#group');
    let semestr_select = $('#semestr');
    let subject_select = $('#subject');

    let teacher_button = $('#add-teacher-button');
    let file_input = $('#file');

    course_select.html('<option value="">----------------</option>')
    course_select.attr('disabled', true)

    direction_select.html('<option value="">----------------</option>')
    direction_select.attr('disabled', true)

    group_select.html('<option value="">----------------</option>')
    group_select.attr('disabled', true)

    semestr_select.html('<option value="">----------------</option>')
    semestr_select.attr('disabled', true)

    subject_select.html('<option value="">----------------</option>')
    subject_select.attr('disabled', true)

    file_input.attr('disabled', true)
    teacher_button.attr('disabled', true)

    if (!faculty) {
        course_select.attr('disabled', true)
        course_select.val('');
        return
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        url: '/data/courses-by-faculty/',
        method: 'GET',
        data: {
            faculty_id: faculty
        },
        success: function(data) {
            let html = course_select.html();

            for (let [k, v] of Object.entries(data)) {
                html += `<option value="${k}">${v}</option>`
            }

            course_select.html(html)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });

    course_select.attr('disabled', false)
})


$(document).on('change', '#course', function() {

    let course = $(this).find(":selected").val();
    let direction_select = $('#direction');
    let group_select = $('#group');
    let semestr_select = $('#semestr');
    let subject_select = $('#subject');

    let teacher_button = $('#add-teacher-button');
    let file_input = $('#file');

    direction_select.html('<option value="">----------------</option>')
    direction_select.attr('disabled', true)

    group_select.html('<option value="">----------------</option>')
    group_select.attr('disabled', true)

    semestr_select.html('<option value="">----------------</option>')
    semestr_select.attr('disabled', true)

    subject_select.html('<option value="">----------------</option>')
    subject_select.attr('disabled', true)

    file_input.attr('disabled', true)
    teacher_button.attr('disabled', true)

    if (!course) {
        direction_select.attr('disabled', true)
        direction_select.val('');
        return
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        url: '/data/directions-by-course/',
        method: 'GET',
        data: {
            course_id: course
        },
        success: function(data) {
            let html = direction_select.html();

            for (let [k, v] of Object.entries(data)) {
                html += `<option value="${k}">${v}</option>`
            }

            direction_select.html(html)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });

    direction_select.attr('disabled', false)
})


$(document).on('change', '#direction', function() {

    let direction = $(this).find(":selected").val();
    let group_select = $('#group');
    let semestr_select = $('#semestr');
    let subject_select = $('#subject');

    let teacher_button = $('#add-teacher-button');
    let file_input = $('#file');

    group_select.html('<option value="">----------------</option>')
    group_select.attr('disabled', true)

    semestr_select.html('<option value="">----------------</option>')
    semestr_select.attr('disabled', true)

    subject_select.html('<option value="">----------------</option>')
    subject_select.attr('disabled', true)

    file_input.attr('disabled', true)
    teacher_button.attr('disabled', true)

    if (!direction) {
        group_select.attr('disabled', true)
        group_select.val('');
        return
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        url: '/data/groups-by-direction/',
        method: 'GET',
        data: {
            direction_id: direction
        },
        success: function(data) {
            let html = group_select.html();

            for (let [k, v] of Object.entries(data)) {
                html += `<option value="${k}">${v}</option>`
            }

            group_select.html(html)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });

    group_select.attr('disabled', false)
})


$(document).on('change', '#group', function() {

    let group = $(this).find(":selected").val();
    let semestr_select = $('#semestr');
    let subject_select = $('#subject');

    let teacher_button = $('#add-teacher-button');
    let file_input = $('#file');

    semestr_select.html('<option value="">----------------</option>')
    semestr_select.attr('disabled', true)

    subject_select.html('<option value="">----------------</option>')
    subject_select.attr('disabled', true)

    file_input.attr('disabled', true)
    teacher_button.attr('disabled', true)

    if (!group) {
        semestr_select.attr('disabled', true)
        semestr_select.val('');
        return
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        url: '/data/semestrs-by-group/',
        method: 'GET',
        data: {
            group_id: group
        },
        success: function(data) {
            let html = semestr_select.html();

            for (let [k, v] of Object.entries(data)) {
                html += `<option value="${k}">${v}</option>`
            }

            semestr_select.html(html)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });

    semestr_select.attr('disabled', false)
})


$(document).on('change', '#semestr', function() {

    let semestr = $(this).find(":selected").val();
    let subject_select = $('#subject');

    let teacher_button = $('#add-teacher-button');
    let file_input = $('#file');

    subject_select.html('<option value="">----------------</option>')
    subject_select.attr('disabled', true)

    file_input.attr('disabled', true)
    teacher_button.attr('disabled', true)

    if (!semestr) {
        subject_select.attr('disabled', true)
        subject_select.val('');
        return
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        url: '/data/subjects-by-semestr/',
        method: 'GET',
        data: {
            semestr_id: semestr
        },
        success: function(data) {
            let html = subject_select.html();

            for (let [k, v] of Object.entries(data)) {
                html += `<option value="${k}">${v}</option>`
            }

            subject_select.html(html)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });

    subject_select.attr('disabled', false)
})


$(document).on('change', '#subject', function() {

    let subject = $(this).find(":selected").val();

    let teacher_button = $('#add-teacher-button');
    let file_input = $('#file');

    
    if (subject) {
        file_input.attr('disabled', false)
        teacher_button.attr('disabled', false)
    } else {
        file_input.attr('disabled', true)
        teacher_button.attr('disabled', true)
    }
})



$(document).on('change', '#t_subject_type', function() {

    let t_subject_type = $(this).find(":selected").val();
    let t_faculty_select = $('#t_faculty');
    let t_department_select = $('#t_department');
    let t_teacher_select = $('#t_teacher');

    if (!t_subject_type) {

        t_faculty_select.val('')
        t_faculty_select.attr('disabled', true)

        t_department_select.val('')
        t_department_select.attr('disabled', true)

        t_teacher_select.val('')
        t_teacher_select.attr('disabled', true)

        return
    }

    t_faculty_select.attr('disabled', false)
})


$(document).on('change', '#t_faculty', function() {

    let t_faculty = $(this).find(":selected").val();
    let t_department_select = $('#t_department');
    let t_teacher_select = $('#t_teacher');

    t_department_select.html('<option value="">----------------</option>')

    t_teacher_select.html('<option value="">----------------</option>')
    t_teacher_select.attr('disabled', true)


    if (!t_faculty) {
        t_department_select.attr('disabled', true)
        t_department_select.val('');
        return
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        url: '/data/departments-by-faculty/',
        method: 'GET',
        data: {
            faculty_id: t_faculty
        },
        success: function(data) {
            let html = t_department_select.html();

            for (let [k, v] of Object.entries(data)) {
                html += `<option value="${k}">${v}</option>`
            }

            t_department_select.html(html)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });

    t_department_select.attr('disabled', false)
})


$(document).on('change', '#t_department', function() {

    let t_department = $(this).find(":selected").val();
    let t_teacher_select = $('#t_teacher');

    t_teacher_select.html('<option value="">----------------</option>')

    if (!t_department) {
        t_teacher_select.attr('disabled', true)
        t_teacher_select.val('');
        return
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        url: '/data/teachers-by-department/',
        method: 'GET',
        data: {
            department_id: t_department
        },
        success: function(data) {
            let html = t_teacher_select.html();

            for (let [k, v] of Object.entries(data)) {
                html += `<option value="${k}">${v}</option>`
            }

            t_teacher_select.html(html)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });

    t_teacher_select.attr('disabled', false)
})

$(document).on('submit', '#add_teacher_form', function(e) {
    e.preventDefault();

    $('#add_teacher_close').click();

    let teachers = $('#teachers').text();
    let _teachers = JSON.parse($('#_teachers').val());
    let subject_type = $('#t_subject_type').find(":selected").val();
    let subject_type_name = $('#t_subject_type').find(":selected").text();
    let teacher = $('#t_teacher').find(":selected").val();
    let teacher_name = $('#t_teacher').find(":selected").text();

    _teachers.push({
        subject_type: subject_type,
        teacher_id: teacher
    })
    $('#_teachers').val(JSON.stringify(_teachers))

    $('#teachers').text(`${teachers}${subject_type_name}: ${teacher_name}\n`)

    $(this)[0].reset()

})