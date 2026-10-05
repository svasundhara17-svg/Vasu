document.addEventListener(
    "DOMContentLoaded",
    () => {

        const age =
            document.querySelector("#age");

        const goal =
            document.querySelector("#goal");


        if (age && goal) {

            age.addEventListener(
                "input",
                () => {

                    document
                        .querySelector(
                            "#minor-note"
                        )
                        ?.remove();


                    if (
                        +age.value > 0 &&
                        +age.value < 18
                    ) {

                        const note =
                            document.createElement(
                                "p"
                            );


                        note.id =
                            "minor-note";


                        note.className =
                            "notice";


                        note.textContent =
                            "For users under 18, FitBuddy focuses on general wellness rather than weight-loss or calorie targets.";


                        goal.parentElement
                            .appendChild(note);

                    }

                }
            );

        }

    }
);