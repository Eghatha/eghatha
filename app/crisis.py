from io import BytesIO
import json
import requests
import streamlit as st
from db.session import get_db
from db import models, schemas
from PIL import Image
import sqlalchemy as sa
from streamlit_chat import message
from annotated_text import annotated_text

logos = [
    "data:image/png;base64,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",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMwAAADACAMAAAB/Pny7AAAAaVBMVEX///8AAACTk5P39/f7+/vW1tY3NzfNzc2hoaHDw8Ps7Ozi4uLy8vK2trYuLi7v7++EhIRxcXGbm5uNjY1CQkIgICA9PT2srKxhYWF7e3slJSUJCQlSUlIQEBDc3NxZWVlKSkppaWkZGRn3XoaeAAAHSUlEQVR4nO2d25qiOhBGWzmLIIKIqIj4/g85OjPdkz8EhRwo9v6yruaiwQpJ6pSqzNeXxWKxWCwWi8VisVgsFovFYrFY/rDxkjwvsqzI88TbUEujgLe+Hvy0bJrLk6YpU/9wLQJqqSRwqnZ1WQm4rNrQoZZuCk5wEo3jH6foPzIed1Ol74fy4lxtXGpJPxNXx89DeeGHN2pZP7BLruOG8uJeLVq9RfX4obyoI2qJB9mG/rSxrFZpvlBNEE+clr+Ts8idE0zYLSz3BS616Cw3ltXqkVDLzpPIDuVFRS094FYDHz312yJMAs8Lkmrd+ulD/HfhkgyocF7K+z6M8e/ian8VLscFzU0kEM/fi03ipqpFCnwxWsDry5Zm0eDKcaNMMJyFhAabQ0+y/fBQXrgCT+EYv3tiLtyeYMfPPteu6n2B/RJ8gZyPwU6jVozX8aNZm5b0MwHv8de7cQ9u+RlNyZXAds+JlI1/ds0vtJGfwRihyloJuRUampJyHDfOu5wwLy8KfPrumZFyJNzE7Kc+n+HzOaVbc0MFe50uC6ZxfMKp4fzLVEKUGzoDhB5nfAdJpOIS9FEPdH4AOphympUzN2SBmgNynCVdxQBShh2VU7OFb1pIiuGg7aRKpcH2l3dGAtABuU4JJwDbP5NeHy5MTapTwglCsDI0CoFvUrJvotk0EGCeFHTqBiwnje8Mq6NQeRO4aBPdO02wrsxZKb2SsNrZ1yXfJBpGAjV/NwbfW5d8U9jBllHati5sGooQ7cYKMNn3R8CVoPCcWQ/xorT/n7qEXbIU2U02LnsoBrwVa2kosjSsZj4rOrsRq84UZ1kKNuJVzRKB50xhaGAwipliiDdrPfJNojY1GPKZ0bnMKGaGdai0KgCKmclNqWYKbfa/MpoQzii6M5DYpAhoNqwA7VblVehokqQ0WAHuSkUjGAIofRdZ2FMmjcEZTUYDFrqSBoAAXHH7SRKwIiglNDr2TTQJWkholgoyJFC0QZTS1JUEhOQMURIQj818aV/TgxMrqgP0eAVSSE6Ni0eJVIWBDti6UjIR4UHe/EpiZV7gqVctJccWz2jpqgJjrM6Qcqrw9C2lOwZ0cpREYr1z30N24+kA17tEXtPBahXV8FsJ7ghvepDIPS97lKgHDw/Ppx7icQUeB+JywLABcS6T4ueKK6alOs/8ZtehPI8JAoUlPnsib9qI+M6f0cHAmivQShdQec4VJo2NBuJeJxdFvozH7UmVJh99gW3UqwZul1Bwytu9F3vvrWSOJygFXkjrSdCTbNXkweBw3CAXtASQV5t+I2prKItEuHfiKBc1CxKXZ7LkAvFWj9O68mD3bG/JuhM2NiygpvkHly+i/Z6ea1e/Wk6eJGFRd+IWjee8LGLzfzPUQPN7RKl/PPppOfwXi2qfeTEwN2NY3FiersDkvsY/LMHw9+nb9DG0i2g1ESDRqEmTjP3M9ibU0O8pPOpuBhHboBho9XtPk0Xknj9PkL1Rve951O+buubmVvT7zibgZ7TtGUB+/yzwew4UR8wi4lPzWdqPXBcxOWNuzBjDmTqd8fW143vOkEvTNOnh1HWng//8p/Dylh9UTt90MHwJQJMe2yzBEM0JkqI9poOr8kgZobnJgEtf3rt1MJAIcIJ1dx/Q42VFFgsMRTGHXrc5TxzuBxTgmuh8hk80/+UUBiNsoBuEnXAHZST+wEboVnbiyF9EnAiVx55gNL3W2d+zEk1SSJtIFDV0s49GNJbL9Bt+NolAFczdFiwaSy1lJuJeenfu0bh9CXz5Nq1+RrSeU0P3dXKnUjvTn+YZ82i9y0zOa7WIpJ/knK22MeDzMEflBEvEx0PlTJ5NLwujw6UKeI/gOo/XyW/+Vsuxqsd/onqOWJrfMK2mqOrWcS+e4WBgx1k5fRHircU3X8wvNO776Ty65/fNVd+rxXDXMum9XiXizKdh/exyBkHzuk4wj5iadTk5Taa9oYK77sRoJpq7AER/ScUWt+TRZDENToyJgiqu6MugsQlwYowYAjxPNJevwQJkU5oTPQH5cukPcMVlhvKpWGBsrAQNV4Cxuh2cf0NODectG7MB6DBdzdTUoPE3GAtiHGtEBexQLxs0zhuYGiN5tBv8hMmriTHt+zChaCCOKY1Wh+HVWpV+w4mZssxoZmsLWexOfy49BofWcIlIBDl1/UEalPsZ0pc/xIav1cErcwxnHF2o9ch0bxqX3ZON8UIkyKc/dA/GgVVm/Jj7ZvQmGtgycj1MkwALrXshwCKeIa29Nvl7bE7Ln6F2DxI1R80vhy0zQ3F4DBlBzS9nX23AJPdwOvYX9f4ghH+zlCLCWbbepQB3TMxy/UjBejR6Y2fWZVa9ymQccOGJ3l+ES2ZmOaJLzN2rA3cZzVJVDe1fencpG8zMc7E6HJyetL6adZXkO/+nAGntVuurWRM2T0NVzA5Gb/K0KtY/5LMUgzjhv18sFvSfoFgsFovFYrFYLBaLxWKxWCwWQn4BSalP1TEihjwAAAAASUVORK5CYII=",
    "data:image/png;base64,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",
]


@st.cache_data
def get_event(event_id: str) -> schemas.Event | None:
    event_id_int = int(event_id)
    db = get_db()
    query = sa.select(models.Event).where(models.Event.id == event_id_int)
    res = db.scalar(query)
    return schemas.Event.model_validate(res) if res else None


@st.cache_data
def get_event_subs_count(event_id: str) -> int:
    event_id_int = int(event_id)
    db = get_db()
    query = sa.select(sa.func.count()).where(
        models.Subscription.event_id == event_id_int
    )
    res = db.scalar(query)
    return res or 0


@st.cache_data
def get_event_owner(event_id: str) -> schemas.User | None:
    event_id_int = int(event_id)
    db = get_db()
    query = (
        sa.select(models.User).join(models.Event).where(models.Event.id == event_id_int)
    )
    res = db.scalar(query)
    return schemas.User.model_validate(res) if res else None


@st.cache_data
def get_event_tags(event_id: str) -> list[schemas.Tags]:
    event_id_int = int(event_id)
    db = get_db()
    query = (
        sa.select(models.Tags)
        .join(models.EventTag)
        .where(models.EventTag.event_id == event_id_int)
    )
    res = db.scalars(query)
    return [schemas.Tags.model_validate(tag) for tag in res.all()]


def get_event_messages(event_id: str) -> list[schemas.Messages]:
    event_id_int = int(event_id)
    db = get_db()
    query = sa.select(models.Messages).where(models.Messages.event_id == event_id_int)
    res = db.scalars(query)
    return [schemas.Messages.model_validate(message) for message in res.all()]


def on_message():
    text = st.session_state["user_input"]
    query = sa.insert(models.Messages).values(
        {"event_id": 1, "text": text, "created_by": 1}
    )
    db = get_db()
    db.execute(query)
    db.commit()


def get_img_path(event_id: str) -> str:
    with open("./links.json", "r") as f:
        links = json.load(f)
    return links[int(event_id) - 1]


@st.cache_data
def get_image(event_id: str) -> Image.Image:
    img_path = get_img_path(event_id)
    response = requests.get(img_path)
    img = Image.open(BytesIO(response.content))
    return img


def crisis(event_id: str):
    event = get_event(event_id)
    if not event:
        st.error("Event not found")
        return

    event_owner = get_event_owner(event_id)
    if not event_owner:
        st.error("Event owner not found")
        return

    st.title(event.title)
    st.subheader("Team Size: " + str(get_event_subs_count(event_id)))
    st.dataframe(
        {
            "Location": event.location,
            "Criticality": event.criticality,
            "Created By": event.created_by,
        },
        use_container_width=True,
    )

    img = get_image(event_id)
    st.image(img, use_column_width=True)

    event_tags = get_event_tags(event_id)
    tags = [tag.text for tag in event_tags]
    tags = [tag for tag in tags for _ in range(2)]
    annotated_text([(tag, "") if i % 2 == 0 else "  " for i, tag in enumerate(tags)])

    st.markdown("---")
    st.subheader("Chat")
    st.write("")

    chat_placeholder = st.empty()

    with chat_placeholder.container():
        messages = get_event_messages(event_id)
        for msg in messages:
            is_me = msg.created_by == 1
            message(msg.text, is_user=is_me, logo=logos[msg.created_by - 1])

    with st.spinner("Loading chat"):
        with st.container():
            st.text_input("User Input:", key="user_input", value="")
            submit = st.button("Submit", on_click=on_message)
            if submit:
                st.rerun()
