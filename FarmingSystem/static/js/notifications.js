(function () {
    const messageElement = document.getElementById('django-messages');

    if (messageElement) {
        const messages = JSON.parse(messageElement.textContent);

        if (window.Swal) {
            (async function showMessages() {
                for (const message of messages) {
                    const tags = message.tags.split(/\s+/);
                    let icon = 'info';

                    if (tags.includes('success')) {
                        icon = 'success';
                    } else if (tags.includes('error')) {
                        icon = 'error';
                    } else if (tags.includes('warning')) {
                        icon = 'warning';
                    }

                    await Swal.fire({
                        toast: true,
                        position: 'top-end',
                        icon: icon,
                        title: message.text,
                        showConfirmButton: false,
                        timer: icon === 'success' ? 3000 : 5000,
                        timerProgressBar: true,
                        customClass: {
                            popup: 'farm-notification'
                        }
                    });
                }
            })();
        } else {
            messages.forEach(function (message) {
                window.alert(message.text);
            });
        }
    }

    document.querySelectorAll('[data-confirm-delete]').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!window.Swal) {
                if (!window.confirm('Delete this farming record? This action cannot be undone.')) {
                    event.preventDefault();
                }
                return;
            }

            event.preventDefault();
            Swal.fire({
                icon: 'warning',
                title: 'Delete this record?',
                text: 'This action cannot be undone.',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it',
                cancelButtonText: 'Keep record',
                confirmButtonColor: '#b42318',
                cancelButtonColor: '#66736b',
                reverseButtons: true,
                focusCancel: true,
                customClass: {
                    popup: 'farm-confirmation'
                }
            }).then(function (result) {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    });
})();
