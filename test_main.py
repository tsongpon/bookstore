from starlette.testclient import TestClient
import unittest
from main import api, connection_pool
from repository.book_repository import BookRepository


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        BookRepository(connection_pool).delete_all_book()

    def test_ping(self):
        client = TestClient(api)
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "ok"}

    def test_query_book_with_empty_data(self):
        client = TestClient(api)
        response = client.get("/v1/books")
        assert response.status_code == 200
        response_body = response.json()
        assert response_body['data'] is not None
        assert response_body['size'] is not None
        assert response_body['total'] is not None

    def test_create_book(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        assert response.status_code == 201
        assert response.json()['id'] is not None
        assert response.json()['created_time'] is not None
        assert response.json()['modified_time'] is not None
        new_book_id = response.json()['id']

    def test_get_none_exist_book(self):
        client = TestClient(api)
        response = client.get("/v1/books/none-exist-key")
        assert response.status_code == 404

    def test_get_book(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        assert response.status_code == 201
        assert response.json()['id'] is not None
        new_book_id = response.json()['id']

        response = client.get("/v1/books/{id}".format(id=new_book_id))
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == new_book_id
        assert data['title'] == "GraphQL in Action"
        assert data['isbn13'] == "9781617295683"
        assert data['paperback_price'] == 49.99
        assert data['ebook_price'] == 39.99
        assert data['category'] == "Programming"
        assert response.json()['created_time'] is not None
        assert response.json()['modified_time'] is not None
        assert 'etag' in response.headers
        assert response.headers['etag'] is not None

    def test_query_book(self):
        client = TestClient(api)
        client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )

        client.post(
            "/v1/books",
            json={
                "title": "Go in Action",
                "synopsis": "Go in Action is for any intermediate-level developer who has experience with other programming languages and wants a jump-start in learning Go or a more thorough understanding of the language and its internals. This book provides an intensive, comprehensive, and idiomatic view of Go. It focuses on the specification and implementation of the language, including topics like language syntax, Go?s type system, concurrency, channels, and testing.",
                "isbn13": "9781617291784",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 44.99,
                "ebook_price": 35.99,
                "category": "Programming"
            },
        )
        response = client.get("/v1/books")
        assert response.status_code == 200
        data = response.json()
        assert 2 == data['size']
        assert 2 == data['total']
        assert data['data'] is not None
        assert 2 == len(data['data'])
        # order by modified_time by default
        assert "Go in Action" == data['data'][0]['title']

    def test_seatch_book(self):
        client = TestClient(api)
        client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )

        client.post(
            "/v1/books",
            json={
                "title": "Go in Action",
                "synopsis": "Go in Action is for any intermediate-level developer who has experience with other programming languages and wants a jump-start in learning Go or a more thorough understanding of the language and its internals. This book provides an intensive, comprehensive, and idiomatic view of Go. It focuses on the specification and implementation of the language, including topics like language syntax, Go?s type system, concurrency, channels, and testing.",
                "isbn13": "9781617291784",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 44.99,
                "ebook_price": 35.99,
                "category": "Programming"
            },
        )
        response = client.get("/v1/books?title=Go in Action")
        assert response.status_code == 200
        data = response.json()
        assert 1 == data['size']
        assert 1 == data['total']
        assert data['data'] is not None
        assert 1 == len(data['data'])
        # order by modified_time by default
        assert "Go in Action" == data['data'][0]['title']

    def test_pagination(self):
        client = TestClient(api)
        client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        client.post(
            "/v1/books",
            json={
                "title": "Go in Action",
                "synopsis": "Go in Action is for any intermediate-level developer who has experience with other programming languages and wants a jump-start in learning Go or a more thorough understanding of the language and its internals. This book provides an intensive, comprehensive, and idiomatic view of Go. It focuses on the specification and implementation of the language, including topics like language syntax, Go?s type system, concurrency, channels, and testing.",
                "isbn13": "9781617291784",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 44.99,
                "ebook_price": 35.99,
                "category": "Programming"
            },
        )
        client.post(
            "/v1/books",
            json={
                "title": "Micro Frontends in Action",
                "synopsis": "Micro Frontends in Action teaches you how to put the theory of micro frontends into practice. Frontend expert Michael Geers teaches you with a complete ecommerce example application that illustrates how a large-scale business application can adopt the micro frontends approach. You’ll learn to integrate web applications made up of smaller fragments using tools such as web components or server side includes, how to solve the organizational challenges of micro frontends, and how to create a design system that ensures an end user gets a consistent look and feel for your application. When you’re done, you’ll be able to better distribute your team’s skills and resources to deliver quality software quickly and flexibly.",
                "isbn13": "9781617296871",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        client.post(
            "/v1/books",
            json={
                "title": "Kubernetes in Action ",
                "synopsis": "Kubernetes in Action teaches you to use Kubernetes to deploy container-based distributed applications. You'll start with an overview of Docker and Kubernetes before building your first Kubernetes cluster. You'll gradually expand your initial application, adding features and deepening your knowledge of Kubernetes architecture and operation. As you navigate this comprehensive guide, you'll explore high-value topics like monitoring, tuning, and scaling.",
                "isbn13": "9781617293726",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 59.99,
                "ebook_price": 47.99,
                "category": "DevOp"
            },
        )

        response = client.get("/v1/books?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert 2 == data['size']
        assert 4 == data['total']
        assert 2 == len(data['data'])

        response = client.get("/v1/books?offset=3")
        assert response.status_code == 200
        data = response.json()
        assert 1 == data['size']
        assert 4 == data['total']
        assert 1 == len(data['data'])

    def test_fulfill_book(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        book_id = response.json()['id']
        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 0 == data['current_amount']

        response = client.post(
            "/v1/books/{id}/fulfill".format(id=book_id),
            json={
                "amount": 100
            },
        )
        assert response.status_code == 200
        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 100 == data['current_amount']

    def test_fulfill_book_with_negative_amount(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        book_id = response.json()['id']
        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 0 == data['current_amount']

        response = client.post(
            "/v1/books/{id}/fulfill".format(id=book_id),
            json={
                "amount": -1
            },
        )
        assert response.status_code == 400
        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 0 == data['current_amount']

    def test_fulfill_none_exist_book(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books/none-exist-book/fulfill",
            json={
                "amount": 1
            },
        )
        assert response.status_code == 404

    def test_sale_book(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        book_id = response.json()['id']
        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 0 == data['current_amount']

        response = client.post(
            "/v1/books/{id}/fulfill".format(id=book_id),
            json={
                "amount": 100
            },
        )

        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 100 == data['current_amount']

        response = client.post(
            "/v1/books/{id}/sale".format(id=book_id),
            json={
                "amount": 10
            },
        )
        assert response.status_code == 200

        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 90 == data['current_amount']

    def test_sale_with_insufficient_amount(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        book_id = response.json()['id']
        response = client.get("/v1/books/{id}".format(id=book_id))
        assert response.status_code == 200
        data = response.json()
        assert 0 == data['current_amount']

        response = client.post(
            "/v1/books/{id}/fulfill".format(id=book_id),
            json={
                "amount": 100
            },
        )
        response = client.post(
            "/v1/books/{id}/sale".format(id=book_id),
            json={
                "amount": 1000
            },
        )
        assert response.status_code == 400
        assert response.json()['message'] == "Insufficient amount"

    def test_sale_none_exist_book(self):
        client = TestClient(api)
        response = client.post(
            "/v1/books/none-exist-book/sale",
            json={
                "amount": 1000
            },
        )
        assert response.status_code == 404

    def test_best_sold_report(self):
        client = TestClient(api)
        graphQL_book_id = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        ).json()['id']
        go_in_action_book_id = client.post(
            "/v1/books",
            json={
                "title": "Go in Action",
                "synopsis": "Go in Action is for any intermediate-level developer who has experience with other programming languages and wants a jump-start in learning Go or a more thorough understanding of the language and its internals. This book provides an intensive, comprehensive, and idiomatic view of Go. It focuses on the specification and implementation of the language, including topics like language syntax, Go?s type system, concurrency, channels, and testing.",
                "isbn13": "9781617291784",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 44.99,
                "ebook_price": 35.99,
                "category": "Programming"
            },
        ).json()['id']
        client.post(
            "/v1/books",
            json={
                "title": "Micro Frontends in Action",
                "synopsis": "Micro Frontends in Action teaches you how to put the theory of micro frontends into practice. Frontend expert Michael Geers teaches you with a complete ecommerce example application that illustrates how a large-scale business application can adopt the micro frontends approach. You’ll learn to integrate web applications made up of smaller fragments using tools such as web components or server side includes, how to solve the organizational challenges of micro frontends, and how to create a design system that ensures an end user gets a consistent look and feel for your application. When you’re done, you’ll be able to better distribute your team’s skills and resources to deliver quality software quickly and flexibly.",
                "isbn13": "9781617296871",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        client.post(
            "/v1/books",
            json={
                "title": "Kubernetes in Action ",
                "synopsis": "Kubernetes in Action teaches you to use Kubernetes to deploy container-based distributed applications. You'll start with an overview of Docker and Kubernetes before building your first Kubernetes cluster. You'll gradually expand your initial application, adding features and deepening your knowledge of Kubernetes architecture and operation. As you navigate this comprehensive guide, you'll explore high-value topics like monitoring, tuning, and scaling.",
                "isbn13": "9781617293726",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 59.99,
                "ebook_price": 47.99,
                "category": "DevOp"
            },
        )

        # fulfill book
        client.post("/v1/books/{id}/fulfill".format(id=go_in_action_book_id),
                    json={
                        "amount": 100
                    }
                    )
        client.post("/v1/books/{id}/fulfill".format(id=graphQL_book_id),
                    json={
                        "amount": 100
                    }
                    )

        # sale book
        client.post("/v1/books/{id}/sale".format(id=go_in_action_book_id),
                    json={
                        "amount": 70
                    }
                    )
        client.post("/v1/books/{id}/sale".format(id=graphQL_book_id),
                    json={
                        "amount": 10
                    }
                    )

        # get report
        report_response = client.get("/v1/books/reports/bestseller")
        assert report_response.status_code == 200
        report_date = report_response.json()
        assert report_date['data'][0]['title'] == "Go in Action"
        assert report_date['data'][0]['sold_amount'] == 70
        assert report_date['data'][0]['category'] == "Programming"

    def test_total_sold_by_category_report(self):
        client = TestClient(api)
        graphQL_book_id = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        ).json()['id']
        go_in_action_book_id = client.post(
            "/v1/books",
            json={
                "title": "Go in Action",
                "synopsis": "Go in Action is for any intermediate-level developer who has experience with other programming languages and wants a jump-start in learning Go or a more thorough understanding of the language and its internals. This book provides an intensive, comprehensive, and idiomatic view of Go. It focuses on the specification and implementation of the language, including topics like language syntax, Go?s type system, concurrency, channels, and testing.",
                "isbn13": "9781617291784",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 44.99,
                "ebook_price": 35.99,
                "category": "Programming"
            },
        ).json()['id']
        client.post(
            "/v1/books",
            json={
                "title": "Micro Frontends in Action",
                "synopsis": "Micro Frontends in Action teaches you how to put the theory of micro frontends into practice. Frontend expert Michael Geers teaches you with a complete ecommerce example application that illustrates how a large-scale business application can adopt the micro frontends approach. You’ll learn to integrate web applications made up of smaller fragments using tools such as web components or server side includes, how to solve the organizational challenges of micro frontends, and how to create a design system that ensures an end user gets a consistent look and feel for your application. When you’re done, you’ll be able to better distribute your team’s skills and resources to deliver quality software quickly and flexibly.",
                "isbn13": "9781617296871",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        )
        kubernetes_in_action_book_id = client.post(
            "/v1/books",
            json={
                "title": "Kubernetes in Action",
                "synopsis": "Kubernetes in Action teaches you to use Kubernetes to deploy container-based distributed applications. You'll start with an overview of Docker and Kubernetes before building your first Kubernetes cluster. You'll gradually expand your initial application, adding features and deepening your knowledge of Kubernetes architecture and operation. As you navigate this comprehensive guide, you'll explore high-value topics like monitoring, tuning, and scaling.",
                "isbn13": "9781617293726",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 59.99,
                "ebook_price": 47.99,
                "category": "DevOp"
            },
        ).json()['id']
        terraform_in_action_book_id = client.post(
            "/v1/books",
            json={
                "title": "Terraform in Action",
                "synopsis": "Terraform in Action unlocks the full potential of infrastructure you can automate, scale, and manage programmatically using Terraform. Through hands-on projects, including deploying a multiplayer game and a fully-managed Kubernetes cluster, distinguished Terraform expert Scott Winkler shows you how to think in Terraform rather than just copy-paste code. Written to focus on Terraform 0.12 and covering new syntax, the book covers both fundamentals and advanced designs, such as zero-downtime deployments and creating your own Terraform provider. When you’re done, you’ll be able to seamlessly manage Terraform cloud architecture and use Terraform as the basis for a continuous development/continuous delivery platform.",
                "isbn13": "9781617296895",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "DevOp"
            }
        ).json()['id']

        # fulfill book
        client.post("/v1/books/{id}/fulfill".format(id=go_in_action_book_id),
                    json={
                        "amount": 100
                    }
                    )
        client.post("/v1/books/{id}/fulfill".format(id=graphQL_book_id),
                    json={
                        "amount": 100
                    }
                    )
        client.post("/v1/books/{id}/fulfill".format(id=kubernetes_in_action_book_id),
                    json={
                        "amount": 100
                    }
                    )
        client.post("/v1/books/{id}/fulfill".format(id=terraform_in_action_book_id),
                    json={
                        "amount": 100
                    }
                    )

        # sale book
        client.post("/v1/books/{id}/sale".format(id=go_in_action_book_id),
                    json={
                        "amount": 70
                    }
                    )
        client.post("/v1/books/{id}/sale".format(id=graphQL_book_id),
                    json={
                        "amount": 10
                    }
                    )
        client.post("/v1/books/{id}/sale".format(id=kubernetes_in_action_book_id),
                    json={
                        "amount": 15
                    }
                    )
        client.post("/v1/books/{id}/sale".format(id=terraform_in_action_book_id),
                    json={
                        "amount": 5
                    }
                    )

        # get report
        report_response = client.get("/v1/books/reports/totalsoldbycategory")
        assert report_response.status_code == 200
        report_date = report_response.json()
        assert report_date[0]['category'] == "Programming"
        assert report_date[0]['total_sold_amount'] == 80
        assert report_date[1]['category'] == "DevOp"
        assert report_date[1]['total_sold_amount'] == 20

    def test_update_book(self):
        client = TestClient(api)
        graphQL_book_id = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        ).json()['id']

        res = client.get("/v1/books/{id}".format(id=graphQL_book_id))
        etag = res.headers['etag']
        created_book = res.json()
        assert created_book['edition'] == "1st"

        put_response = client.put(
            "/v1/books/{id}".format(id=graphQL_book_id),
            json={
                "id": graphQL_book_id,
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "First Edition",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
            headers={"If-Match": etag}
        )
        assert put_response.status_code == 200
        res = client.get("/v1/books/{id}".format(id=graphQL_book_id))
        updated_book = res.json()
        assert updated_book['edition'] == "First Edition"

    def test_update_book_with_precondition_fail(self):
        client = TestClient(api)
        graphQL_book_id = client.post(
            "/v1/books",
            json={
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "1st",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
        ).json()['id']
        res = client.get("/v1/books/{id}".format(id=graphQL_book_id))
        etag = res.headers['etag']
        created_book = res.json()
        assert created_book['edition'] == "1st"

        put_response = client.put(
            "/v1/books/{id}".format(id=graphQL_book_id),
            json={
                "id": graphQL_book_id,
                "title": "GraphQL in Action",
                "synopsis": "GraphQL in Action, you’ll learn to use GraphQL to simplify interactions with your web servers and improve the performance of your data APIs. Twenty-year web development veteran Samer Buna starts by introducing GraphQL’s unique query-based API paradigm, laying out its unique design concepts and advantages over traditional APIs. From there, you’ll master the GraphQL way of creating APIs for hierarchical data, unlock easy ways to incorporate GraphQL into your existing codebase, and learn how to consume a GraphQL API with queries, mutations, and subscriptions using the GraphQL query language. When you’re done, you’ll have all the skills you need to get started writing and using scalable data APIs with GraphQL. GraphQL is a new paradigm. ",
                "isbn13": "9781617295683",
                "language": "english",
                "publisher": "manning",
                "edition": "First Edition",
                "paperback_price": 49.99,
                "ebook_price": 39.99,
                "category": "Programming"
            },
            headers={"If-Match": "outdated-etag-cos-someone-just-update-this-book"}
        )
        assert put_response.status_code == 412

        res = client.get("/v1/books/{id}".format(id=graphQL_book_id))
        book = res.json()
        assert book['edition'] == "1st"


if __name__ == '__main__':
    unittest.main()
